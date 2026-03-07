from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    message = f"""
🤖 TalentAI Recruitment Bot

Your Telegram Chat ID is:

{chat_id}

Please copy this ID and paste it in the job application form to receive interview notifications.
"""

    await update.message.reply_text(message)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()