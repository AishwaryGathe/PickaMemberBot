from telegram import Update
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes
import os, random

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set!")

application = Application.builder().token(BOT_TOKEN).build()

members = set()  # store unique members

# Track members joining
async def track_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member.new_chat_member
    if chat_member.status in ["member", "administrator"]:
        user = chat_member.user.first_name
        members.add(user)

# Pick random member
async def pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not members:
        await update.message.reply_text("No members tracked yet.")
    else:
        choice = random.choice(list(members))
        await update.message.reply_text(f"🎯 Picked: {choice}")

application.add_handler(ChatMemberHandler(track_member, ChatMemberHandler.CHAT_MEMBER))
application.add_handler(CommandHandler("pick", pick))

if __name__ == "__main__":
    application.run_polling()
