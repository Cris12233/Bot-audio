import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Configurar logs para ver actividad en Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def manejar_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message
    
    # Obtener el objeto de audio o documento
    audio_obj = mensaje.audio or mensaje.document
    if not audio_obj:
        await mensaje.reply_text("Por favor, envíame un archivo de audio.")
        return

    await mensaje.reply_text("🔄 Procesando y actualizando el nombre de tu audio...")

    # 1. Descargar el archivo de Telegram
    archivo = await audio_obj.get_file()
    ruta_temporal = "temp_audio.mp3"
    await archivo.download_to_drive(ruta_temporal)

    # 2. Obtener el nombre original limpio
    nombre_limpio = audio_obj.file_name or "cancion.mp3"
    
    # 3. Reenviar con la propiedad filename para conservar el nombre real al descargar
    with open(ruta_temporal, 'rb') as f:
        await mensaje.reply_audio(
            audio=f,
            title=nombre_limpio.replace(".mp3", ""),
            filename=nombre_limpio
        )

    # 4. Eliminar el archivo temporal del servidor
    if os.path.exists(ruta_temporal):
        os.remove(ruta_temporal)

if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("❌ Error: No se configuró la variable TELEGRAM_TOKEN.")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.AUDIO | filters.Document.AUDIO, manejar_audio))

    print("🤖 Bot iniciado correctamente...")
    app.run_polling()
  
