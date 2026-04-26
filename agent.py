from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from tools import *
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

THREAD_ID = "1"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

tools = [add_task_tool,
        list_tasks_tool,
        set_task_done_tool,
        remove_task_tool,
        add_grocery_tool,
        list_groceries_tool,
        set_grocery_done_tool,
        remove_grocery_tool,
        add_note_tool,
        list_notes_tool,
        set_note_done_tool,
        remove_note_tool,
        delete_done_tool,
        search_schedule_tool,
        ]

system_message = SystemMessage("""
You are a personal assistant. Be concise and accurate.

You can:
- manage tasks
- manage groceries
- manage notes
- answer questions about the schedule

Always use tools when needed.
If there is an item that makes sens to remember, use a tool and store it.
If the user wants to remove an item use a tool and remove it.
If the user wants to store something, use a tool and store it..
If the user asks about schedule, use search_schedule_tool.
If the user asks about anything where the schedule could be relevant, inform the user.

""")

#middelware ... TODO

model =  ChatOpenAI(model="gpt-4o-mini", temperature=0.1, max_tokens=1000)
agent = create_agent(model=model, tools=tools, system_prompt=system_message ,checkpointer=InMemorySaver())

def invoke_agent(user_message: str) -> dict[str, Any]:
    human_message = HumanMessage(user_message)
    result = agent.invoke(
        {"messages": [human_message]},
        {"configurable": {"thread_id": THREAD_ID}},
    )
    return result