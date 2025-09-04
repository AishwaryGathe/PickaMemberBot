import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random

# use PORT from Render
PORT = int(os.environ.get("PORT", 8080))

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set!")

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is alive on Render"

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

# Telegram bot logic
application = Application.builder().token(BOT_TOKEN).build()
members = []

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    if user not in members:
        members.append(user)
        await update.message.reply_text(f"{user} added!")

async def pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not members:
        await update.message.reply_text("No members yet.")
    else:
        choice = random.choice(members)
        await update.message.reply_text(f"🎯 Picked: {choice}")

application.add_handler(CommandHandler("add", add))
application.add_handler(CommandHandler("pick", pick))

if __name__ == "__main__":
    Thread(target=run_flask).start()
    application.run_polling()
