import os
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


def main():
    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        MessageHandler(filters.Document.PDF, handle_document)
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Telegram bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()


