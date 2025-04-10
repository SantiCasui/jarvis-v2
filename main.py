import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Cargar token y URL desde variables de entorno
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Ej: https://tubot.onrender.com/webhook

app = Flask(__name__)

# Crear aplicación de telegram
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot 🤖.")

# Otros comandos
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hola {update.effective_user.first_name} 👋")

# Añadir handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("hello", hello))

# Webhook para recibir actualizaciones de Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"

# Endpoint para establecer el webhook (solo una vez)
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    telegram_app.bot.set_webhook(url=WEBHOOK_URL + "/webhook")
    return "Webhook configurado"

# Inicio manual local
if __name__ == "__main__":
    app.run(port=5000)
