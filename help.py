from telegram import Update
from telegram.ext import ContextTypes
from utils.banner import HELP_TEXT

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)
