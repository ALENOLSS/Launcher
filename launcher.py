import subprocess
import sys
import time
import os

# -----------------------------
# Step 1: Ensure dependencies are installed
requirements = [
    "python-telegram-bot==20.3",
    "aiohttp==3.8.5"
]

for package in requirements:
    subprocess.run([sys.executable, "-m", "pip", "install", package])

# -----------------------------
# Step 2: Write bot.py dynamically
bot_code = '''
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8190987979:AAGqLQxym3_45oM0W1hhwfl2t0XTM4ZUOT4"
CHANNEL_ID = -1002678391495
ADMIN_ID = 7282835498

ASK_TEXT, ASK_BTN_TEXT, ASK_BTN_URL, CONFIRM = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Access Denied! Only admin can use this bot.")
        return ConversationHandler.END
    await update.message.reply_text("✍️ Send message text:")
    return ASK_TEXT

async def get_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["msg_text"] = update.message.text
    await update.message.reply_text("🔘 Send button text:")
    return ASK_BTN_TEXT

async def get_button_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["btn_text"] = update.message.text
    await update.message.reply_text("🌐 Send button URL:")
    return ASK_BTN_URL

async def get_button_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["btn_url"] = update.message.text
    keyboard = [[InlineKeyboardButton("✅ Yes", callback_data="yes"),
                 InlineKeyboardButton("❌ No", callback_data="no")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚠ Post to channel?", reply_markup=reply_markup)
    return CONFIRM

async def confirm_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "yes":
        msg_text = context.user_data["msg_text"]
        btn_text = context.user_data["btn_text"]
        btn_url = context.user_data["btn_url"]
        keyboard = [[InlineKeyboardButton(btn_text, url=btn_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=CHANNEL_ID, text=msg_text, reply_markup=reply_markup)
        await query.edit_message_text("✅ Posted successfully!")
    else:
        await query.edit_message_text("❌ Cancelled.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_text)],
            ASK_BTN_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_button_text)],
            ASK_BTN_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_button_url)],
            CONFIRM: [CallbackQueryHandler(confirm_post)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
'''

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(bot_code)

# -----------------------------
# Step 3: Run the bot in an infinite loop to stay 24/7
while True:
    try:
        print("🔁 Starting bot...")
        subprocess.run([sys.executable, "bot.py"])
    except Exception as e:
        print(f"⚠ Bot crashed: {e}")
        time.sleep(5)  # wait 5 sec before restart