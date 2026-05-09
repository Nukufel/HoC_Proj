import os
import base64
import tempfile
from dotenv import load_dotenv
from openai import OpenAI
from agent import invoke_agent
from tools import _rag

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

_vision_client = OpenAI()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    print(f"User: {text}")

    result = invoke_agent(text)
    reply = result["messages"][-1].content
    print(f"Agent: {reply}")

    await update.message.reply_text(reply)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if doc.file_name != "pdf":
        await update.message.reply_text("Only PDF are supported.")
        return

    file = await doc.get_file()
    file_name = doc.file_name or "uploaded.pdf"
    local_path = os.path.join("resources", file_name)
    await file.download_to_drive(local_path)

    print(f"📄 PDF received: {file_name}")
    _rag.add_pdf(local_path)
    await update.message.reply_text(f"PDF '{file_name}' has been added to the document store.")



async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    local_path = os.path.join(tempfile.gettempdir(), f"{photo.file_id}.jpg")
    await file.download_to_drive(local_path)

    with open(local_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    print(f"🖼️ Photo received: {photo.file_id}")

    vision_response = _vision_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze this image. It may contain a schedule/timetable, "
                            "grocery list, or notes. Extract all information "
                            "precisely. For schedules: list each event with title, date, "
                            "time, and location if visible. For grocery lists: list every "
                            "item. For notes: transcribe the full text. "
                            "Return structured plain text only."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                    },
                ],
            }
        ],
        max_tokens=1000,
    )

    extracted = vision_response.choices[0].message.content
    print(f"Vision extraction:\n{extracted}")

    result = invoke_agent(
        f"I just analyzed an uploaded image. Here is the extracted information:\n\n"
        f"{extracted}\n\n"
        f"Please store everything in the database using the appropriate tools."
    )
    reply = result["messages"][-1].content
    print(f"Agent: {reply}")
    await update.message.reply_text(reply)


def main():
    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        MessageHandler(filters.Document.PDF, handle_document)
    )
    """
    app.add_handler(
        MessageHandler(filters.PHOTO, handle_photo)
    )
    """

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Telegram bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()


