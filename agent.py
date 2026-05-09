from typing import Any
from rag import RAG
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from tools import *
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.agents.middleware.summarization import SummarizationMiddleware
from langchain.agents.middleware import AgentMiddleware
import datetime
from dateparser.search import search_dates


RAG = RAG()


THREAD_ID = "1"

class RAGMiddleware(AgentMiddleware):

    def before_model(self, state, config):
        if not config.get("configurable", {}).get("use_rag"):
            return state

        query = next(
            (m.content for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
            None,
        )
        if not query:
            return state

        rag_result = RAG.search(query)
        if rag_result:
            rag_message = SystemMessage(
                content=(
                    f"The following was retrieved from the user's uploaded documents "
                    f"and is relevant to the question. Use this to answer accurately.\n\n"
                    f"DOCUMENT CONTEXT: \n{rag_result}\n END CONTEXT \n\n"
                )
            )
            state["messages"] = [rag_message] + state["messages"]

        return state

def sanitize_dates(text: str) -> str:
    results = search_dates(text, settings={"PREFER_DATES_FROM": "future", "RETURN_AS_TIMEZONE_AWARE": False})
    if not results:
        return text
    for date_string, date_obj in results:
        text = text.replace(date_string, date_obj.strftime("%Y-%m-%d %H:%M"), 1)
    print(text)
    return text

def get_current_datetime() -> str:
    now = datetime.datetime.now()
    return f"Current datetime: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

TOOLS = [
        add_event_tool,
        get_events_tool,
        delete_event_by_id_tool,
        update_user_name_tool,
        update_user_birthdate_tool,
        get_user_tool,
        add_grocery_tool,
        list_groceries_tool,
        set_grocery_done_tool,
        remove_grocery_tool,
        add_note_tool,
        list_notes_tool,
        set_note_done_tool,
        remove_note_tool,
        delete_done_tool,
        ]


SYSTEM_PROMPT = SystemMessage("""
You are a personal assistant. Be concise and accurate.

You can:
- manage tasks
- manage groceries
- manage notes
- answer questions about the schedule

If you don't have the information to answer a question, use tools to retrieve it first.
If the user requests information, use tools to retrieve it.
You may call multiple tools sequentially.
Never guess event IDs or IDs in general.


Always use tools when needed.
Rules:
- When using a tool read the description of the tools first to determine the right tool to use.
- If you don't have some information inform the user about that.
- If the user asks about his persona information use the get_user_tool.
- If there is an item that makes sens to remember, use a tool and store it.
- If the user wants to remove an item use a tool and remove it.
- If the user wants to store something, use a tool and store it.
- If the user asks about anything where the schedule could be relevant, use a tool and infor him.
- If the user talks about an event use a tool and store the evet in his events.
- If a tool does not retrieve the requested information use a different tool or tell the user the information is missing.
""")

model =  ChatOpenAI(model="gpt-4o-mini", temperature=0.1, max_tokens=3000)

summarizer = SummarizationMiddleware(
    model=model,
    trigger=[("tokens", 2000)]
)

ragMiddleware = RAGMiddleware()

MIDDLEWARES = [
    summarizer,
    ragMiddleware,
]

agent = create_agent(model=model, tools=TOOLS, system_prompt=SYSTEM_PROMPT, middleware=MIDDLEWARES, checkpointer=InMemorySaver())

def invoke_agent(user_message: str, use_rag: bool = False, context: str = None) -> dict[str, Any]:
    messages = []

    messages.append(SystemMessage(get_current_datetime()))
    if context: messages.append(SystemMessage(context))
    messages.append(HumanMessage(sanitize_dates(user_message)))

    result = agent.invoke(
        {"messages": messages},
        {"configurable": {"thread_id": THREAD_ID, "use_rag": use_rag}},
    )
    return result