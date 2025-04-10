from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os

# API de precios
API_KEY = '354c41fa243c4677a4491f35884d1fcb'
BASE_URL = 'https://financialmodelingprep.com/api/v3/quote/'

# Activos disponibles
SIMBOLOS = {
    'btc': 'BTCUSD',
    'oro': 'XAUUSD',
    'nasdaq': '^IXIC',
    'eurusd': 'EURUSD',
    'eurjpy': 'EURJPY',
    'usdjpy': 'USDJPY'
}

# Obtener precio actual
def obtener_precio(simbolo):
    try:
        url = f"{BASE_URL}{simbolo}?apikey={API_KEY}"
        respuesta = requests.get(url)
        datos = respuesta.json()
        if datos and 'price' in datos[0]:
            precio = datos[0]['price']
            return f"💰 El precio actual de {simbolo} es: ${precio:.2f}"
        else:
            return "❌ No se pudo obtener el precio en este momento."
    except Exception as e:
        return f"⚠️ Error: {e}"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("¿En qué puedo servirle, señor?")

# /precio
async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        activo = context.args[0].lower()
        if activo in SIMBOLOS:
            simbolo = SIMBOLOS[activo]
            mensaje = obtener_precio(simbolo)
        else:
            mensaje = "❗ Activo no reconocido. Usa: btc, oro, nasdaq, eurusd, eurjpy, usdjpy."
    except IndexError:
        mensaje = "❗ Escribe el activo. Ej: /precio btc"
    await update.message.reply_text(mensaje)

# Iniciar aplicación
if __name__ == '__main__':
    TOKEN = os.environ.get('BOT_TOKEN')  # En Render debes definir esta variable de entorno
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))

    app.run_polling()
