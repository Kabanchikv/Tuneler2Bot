import uvicorn
import asyncio
from fastapi import FastAPI
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from app.config import settings
from app.database import init_db
from app.bot.core import dp, bot
from app.webhooks import cryptocloud_router, yookassa_router
from app.admin import router as admin_router
from app.tasks import start_background_tasks
from aiogram.types import FSInputFile

app = FastAPI()

# Включаем роутеры
app.include_router(cryptocloud_router, prefix="/webhooks")
app.include_router(yookassa_router, prefix="/webhooks")
app.include_router(admin_router, prefix="/admin")

@app.on_event("startup")
async def on_startup():
    # Инициализация базы данных
    await init_db()
    
    # Настройка вебхука
    await bot.set_webhook(
        url=f"{settings.BASE_WEBHOOK_URL}{settings.WEBHOOK_PATH}",
        certificate=FSInputFile(settings.SSL_CERT_PATH) if settings.SSL_CERT_PATH else None,
        secret_token=settings.WEBHOOK_SECRET
    )
    
    # Запуск фоновых задач
    await start_background_tasks()
    
    print("Bot started")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    print("Bot stopped")

# Регистрируем обработчик Telegram
webhook_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
    secret_token=settings.WEBHOOK_SECRET
)
webhook_handler.register(app, path=settings.WEBHOOK_PATH)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ssl_keyfile=settings.SSL_KEY_PATH,
        ssl_certfile=settings.SSL_CERT_PATH
    )