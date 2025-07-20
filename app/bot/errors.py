from aiogram import Dispatcher
from aiogram.types import ErrorEvent
import logging

logger = logging.getLogger(__name__)

async def handle_telegram_error(event: ErrorEvent):
    logger.error(f"Telegram error: {event.exception}", exc_info=True)
    try:
        await event.update.message.answer("❌ Произошла ошибка. Пожалуйста, попробуйте позже.")
    except:
        pass

def register_error_handlers(dp: Dispatcher):
    dp.errors.register(handle_telegram_error)