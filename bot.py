import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN
from handlers.commands import top_movies, button_handler
from services.scheduler_service import start_scheduler

# Carrega as variáveis de ambiente
load_dotenv()

async def main():
    # 1. Configura o Bot usando o Token do seu config.py
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # 2. Registra os comandos (Handlers)
    application.add_handler(CommandHandler("top", top_movies))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^page_"))
    
    # 3. Inicia o agendador de alertas
    start_scheduler()
    
    # 4. Inicia o bot
    async with application:
        await application.initialize()
        await application.start()
        # Comando correto para a versão 20
        await application.updater.start_polling()
        
        print("🚀 Bot iniciado e monitorando tendências...")
        print("Pressione Ctrl+C para parar.")
        
        # Mantém o bot vivo
        while True:
            await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        # Esse é o jeito certo de ligar no Python 3.12
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot desligado com sucesso.")
