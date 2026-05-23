import os
from dotenv import load_dotenv
from agent import invoke_agent, RAG
from image_handler import ImageHandler
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters, CommandHandler


load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

_image_handler = ImageHandler()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    print(f"User: {text}")

    result = invoke_agent(text)
    reply = result["messages"][-1].content
    print(f"Agent: {reply}")

    await update.message.reply_text(reply)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # largest available resolution
    file = await photo.get_file()
    image_bytes = bytes(await file.download_as_bytearray())
    caption = update.message.caption or ""

    print("Image received, analyzing...")

    extracted = _image_handler.extract(image_bytes, user_hint=caption)
    print(f"Vision extracted: {extracted}")

    agent_instruction = (
        "Store every item from the image analysis below using the appropriate tool. "
        "Add each item separately. Do not skip any item."
    )
    if caption:
        agent_instruction += f" The user's note: \"{caption}\""

    result = invoke_agent(
        agent_instruction,
        context=f"Image analysis result:\n{extracted}",
    )
    reply = result["messages"][-1].content
    print(f"Agent: {reply}")
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Telegram bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()


