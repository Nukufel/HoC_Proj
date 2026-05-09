import os
from dotenv import load_dotenv
from openai import OpenAI
from agent import invoke_agent, RAG
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters, CommandHandler


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
    file = await doc.get_file()
    file_name = doc.file_name or "uploaded.pdf"
    local_path = os.path.join("resources", file_name)
    await file.download_to_drive(local_path)

    print(f"📄 PDF received: {file_name}")
    RAG.add_pdf(local_path)
    await update.message.reply_text(f"PDF '{file_name}' has been added to the document store.")


async def handle_fs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).strip()

    if not query:
        await update.message.reply_text("Please provide a question. Example: /fs what is XSS?")
        return

    print(f"User [/fs]: {query}")
    result = invoke_agent(query, use_rag=True)
    reply = result["messages"][-1].content
    print(f"Agent: {reply}")
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.Document.PDF, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("fs", handle_fs_command))

    print("✅ Telegram bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()


