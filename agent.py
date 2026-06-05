from typing import Any
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from tools import *
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.agents.middleware.summarization import SummarizationMiddleware
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    before_model,
    PIIMiddleware,
)
from datetime import datetime
from dateparser.search import search_dates
from memory.database import update_reoccurring_events


DAYS = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
]


@before_model
def advance_date(state, runtime):
    update_reoccurring_events()


def sanitize_dates(text: str) -> str:
    results = search_dates(
        text,
        settings={
            'PREFER_DATES_FROM': 'future',
            'RETURN_AS_TIMEZONE_AWARE': False,
        },
    )
    if not results:
        return text
    for date_string, date_obj in results:
        text = text.replace(
            date_string, date_obj.strftime('%Y-%m-%d %H:%M'), 1
        )
    return text


def get_current_datetime() -> str:
    now = datetime.now()
    return f'Current datetime: {DAYS[now.weekday()]} the {now}'


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


SYSTEM_PROMPT = SystemMessage(
    """
    You are a personal assistant that helps the user manage their daily life.
    Be concise and friendly.
    You are ment to store and provide information.
    
    Do not ask followup questions.
    Do not tell the user things like "If you need anything else, just let me know!"
    Do not provide unnecessary information.
    
    ## Capabilities
    - **Calendar**: add, list, and delete events (meetings, appointments, lectures, deadlines)
    - **Groceries**: add, list, mark done, and remove items from the shopping list
    - **Notes**: save, list, mark done, and delete notes, reminders, and to-dos
    - **Profile**: store and retrieve the user's name and birthdate
    
    ## Tool rules
    - If somthing is unclear ask the user.
    - Always call a tool to retrieve data before answering questions about it — never guess.
    - To delete or update any item, first call the relevant list/get tool to find the correct ID.
    - Never invent or assume an ID.
    - If the user mentions their name or birthdate, save it immediately with the appropriate tool.
    - If the user describes an upcoming event, save it immediately with add_event_tool.
    - If something belongs on the grocery list or in notes, save it proactively without being asked.
    - If a tool returns no data, tell the user — do not fabricate information.
    - You may call multiple tools in sequence to complete a single request.
    """
)

model = ChatOpenAI(model='gpt-4o-mini', temperature=0.1, max_tokens=5000)

summarizer = SummarizationMiddleware(
    model=model, trigger=[('messages', 20), ('tokens', 4000)]
)
callLimit = ModelCallLimitMiddleware(thread_limit=20, run_limit=10)
guard = PIIMiddleware(
    'api_key',
    detector=r'sk-[a-zA-Z0-9]{32}',
    strategy='block',
    apply_to_input=True,
)

MIDDLEWARES = [
    summarizer,
    advance_date,
    callLimit,
    guard,
]

agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
    middleware=MIDDLEWARES,
    checkpointer=InMemorySaver(),
)


def invoke_agent(
    user_message: str, use_rag: bool = False, context: str = None
) -> dict[str, Any]:
    messages = []

    messages.append(SystemMessage(get_current_datetime()))
    if context:
        messages.append(SystemMessage(context))
    messages.append(HumanMessage(sanitize_dates(user_message)))

    result = agent.invoke(
        {'messages': messages},
        {'configurable': {'thread_id': 0, 'use_rag': use_rag}},
    )
    return result
