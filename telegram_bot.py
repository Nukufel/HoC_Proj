import os
import pytz
from datetime import time
from dotenv import load_dotenv
from agent import invoke_agent
from image_handler import ImageHandler
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
TZ = pytz.timezone('Europe/Zurich')
CHAT_ID = os.getenv('CHAT_ID') if os.getenv('CHAT_ID') else None

_image_handler = ImageHandler()

def get_chat_id(update: Update):
    global CHAT_ID
    if CHAT_ID is None or CHAT_ID != update.message.chat_id:
        CHAT_ID = update.effective_chat.id
        with open('.env', 'a') as f:
            f.write(f'\nCHAT_ID={CHAT_ID}')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get_chat_id(update)

    text = update.message.text
    print(f'User: {text}')

    result = invoke_agent(text)
    reply = result['messages'][-1].content
    print(f'Agent: {reply}')

    await update.message.reply_text(reply)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get_chat_id(update)

    photo = update.message.photo[-1]  # largest available resolution
    file = await photo.get_file()
    image_bytes = bytes(await file.download_as_bytearray())
    caption = update.message.caption or ''

    print('Analyzing image')

    extracted = _image_handler.extract(image_bytes, text=caption)
    print(f'Vision extracted: {extracted}')

    agent_instruction = (
        'Add every calendar event from the image analysis below using the add_event tool. '
        'Add each event separately. Do not skip any event.'
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
        "Send a good morning message. "
        "Include today's events. "
        "Keep it short and friendly."
    )
    reply = result['messages'][-1].content
    print(f'Morning message: {reply}')
    await context.bot.send_message(chat_id=CHAT_ID, text=reply)


def main():
    app = Application.builder().token(TOKEN).build()

    app.job_queue.run_daily(send_morning_message, time=time(hour=10, minute=12, tzinfo=TZ))

    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print('✅ Telegram bot running...')
    app.run_polling()


if __name__ == '__main__':
    main()
