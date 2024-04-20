import os
import sys
from os import path
import logging
from dotenv import load_dotenv

import telegram
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update, context):
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text="Hi there, how can i help?")


async def get_info(update, context):
    chat_id = update.message.chat_id
    try:
        sheets_info = handler.return_root()
        reply_text = f"Sheets info:\nTotal counts: {len(sheets_info['info']['sheet_list'])}"
        await context.bot.send_message(chat_id=chat_id, text=reply_text)
    except telegram.error.TimedOut as error:
        await context.bot.send_message(chat_id=chat_id, text="Oops, there was an error. Please try later.")


def main():

    load_dotenv()
    TOKEN = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_info", get_info))
    application.run_polling()
    return True


if __name__ == "__main__":
    sys.path.append(path.dirname("D:/project/sheet engine/"))
    from SheetEngine import Handler
    handler = Handler(sheet_path="D:/project/sheet engine/sheets.json")
    main()
