import asyncio
import logging
from datetime import datetime
from .database import async_session
from .crud import get_expired_subscriptions, deactivate_subscription

logger = logging.getLogger(__name__)

async def check_subscriptions():
    """Проверяет и деактивирует просроченные подписки"""
    while True:
        try:
            async with async_session() as db:
                expired_subs = await get_expired_subscriptions(db)
                for sub in expired_subs:
                    await deactivate_subscription(db, sub.id)
                    logger.info(f"Subscription deactivated: {sub.id}")
                await db.commit()
        except Exception as e:
            logger.error(f"Subscription check error: {str(e)}")
        
        # Запускаем проверку раз в час
        await asyncio.sleep(3600)

async def start_background_tasks():
    """Запускает все фоновые задачи"""
    asyncio.create_task(check_subscriptions())