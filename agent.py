import datetime
from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from tools import *
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.agents.middleware.summarization import SummarizationMiddleware
from langchain.agents.middleware import AgentMiddleware
import datetime


THREAD_ID = "1"

class DateTimeMiddleware(AgentMiddleware):

    def before_model(self, state, config):
        now = datetime.datetime.now()

        datetime_message = SystemMessage(
            content=f"Current datetime: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )

        state["messages"] = [datetime_message] + state["messages"]

        return state

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
        search_documents_tool,
        ]


SYSTEM_MESSAGE = SystemMessage("""
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

datetimeMiddleware = DateTimeMiddleware()

MIDDLEWARES = [
    summarizer,
    datetimeMiddleware,
]


agent = create_agent(model=model, tools=TOOLS, system_prompt=SYSTEM_MESSAGE, middleware=MIDDLEWARES, checkpointer=InMemorySaver())

def invoke_agent(user_message: str) -> dict[str, Any]:
    human_message = HumanMessage(user_message)
    result = agent.invoke(
        {"messages": [human_message]},
        {"configurable": {"thread_id": THREAD_ID}},
    )
    return result