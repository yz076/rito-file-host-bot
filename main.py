from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1003894895503"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any file and I will give you a permanent link!")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    f = msg.document or msg.video or msg.audio or (msg.photo[-1] if msg.photo else None)
    if not f:
        await msg.reply_text("Unsupported file type!")
        return
    await msg.reply_text("Uploading...")
    try:
        sent = await context.bot.send_document(chat_id=CHANNEL_ID, document=f.file_id)
        link = f"https://t.me/c/3894895503/{sent.message_id}"
        await msg.reply_text(f"Done! Your permanent link: {link}")
    except Exception as e:
        await msg.reply_text(f"Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.PHOTO, handle_file))
    print("Bot is running!")
    app.run_polling()

if __name__ == "__main__":
    main()
