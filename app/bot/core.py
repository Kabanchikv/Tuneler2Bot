from aiogram import Bot, Dispatcher
from .handlers import router as bot_router
from .errors import register_error_handlers
from app.config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

dp.include_router(bot_router)
register_error_handlers(dp)