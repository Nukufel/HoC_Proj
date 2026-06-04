import os
from datetime import time
from dotenv import load_dotenv
from agent import invoke_agent
from image_handler import ImageHandler
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

_image_handler = ImageHandler()
_chat_id = CHAT_ID


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global _chat_id
    if _chat_id is None:
        _chat_id = update.effective_chat.id

    text = update.message.text
    print(f'User: {text}')

    result = invoke_agent(text)
    reply = result['messages'][-1].content
    print(f'Agent: {reply}')

    await update.message.reply_text(reply)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global _chat_id
    if _chat_id is None:
        _chat_id = update.effective_chat.id

    photo = update.message.photo[-1]  # largest available resolution
    file = await photo.get_file()
    image_bytes = bytes(await file.download_as_bytearray())
    caption = update.message.caption or ''

    print('Image received, analyzing...')

    extracted = _image_handler.extract(image_bytes, user_hint=caption)
    print(f'Vision extracted: {extracted}')

    agent_instruction = (
        'Store every item from the image analysis below using the appropriate tool. '
        'Add each item separately. Do not skip any item.'
    )
    if caption:
        agent_instruction += f' The user\'s note: "{caption}"'

    result = invoke_agent(
        agent_instruction,
        context=f'Image analysis result:\n{extracted}',
    )
    reply = result['messages'][-1].content
    print(f'Agent: {reply}')
    await update.message.reply_text(reply)


async def send_morning_message(context: ContextTypes.DEFAULT_TYPE):
    result = invoke_agent(
        'Send a good morning message. '
        "Include today's events and all open tasks/notes. "
        'Keep it short and friendly.'
    )
    reply = result['messages'][-1].content
    print(f'Morning message: {reply}')
    await context.bot.send_message(chat_id=_chat_id, text=reply)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    app.job_queue.run_daily(send_morning_message, time=time(hour=7, minute=0))

    print('✅ Telegram bot running...')
    app.run_polling()


if __name__ == '__main__':
    main()
