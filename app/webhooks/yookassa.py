from fastapi import APIRouter, Request, HTTPException
from app.database import async_session
from app.crud import get_subscription_by_payment_id, update_subscription
from app.frp.utils import generate_frp_config, save_toml_file
from app.bot.core import bot
from aiogram.types import FSInputFile
from .config import settings
import os

router = APIRouter()

@router.post("/yookassa")
async def yookassa_webhook(request: Request):
    data = await request.json()
    
    # Проверка вебхука
    if not verify_yookassa_webhook(data):
        raise HTTPException(status_code=400, detail="Invalid webhook")
    
    # Обработка успешного платежа
    payment_id = data['object']['id']
    order_id = data['object']['metadata'].get('order_id')
    
    if not order_id:
        return {"status": "error", "message": "Order ID not found"}
    
    async with async_session() as db:
        subscription = await get_subscription_by_payment_id(db, order_id)
        if not subscription:
            return {"status": "error", "message": "Subscription not found"}
        
        # Активируем подписку
        await update_subscription(db, subscription.id, {"is_active": True})
        
        # Генерируем FRP конфиг
        config = generate_frp_config(subscription.subdomain)
        filename = save_toml_file(subscription.subdomain, config)
        
        # Отправляем файл пользователю
        file = FSInputFile(filename)
        await bot.send_document(
            chat_id=subscription.user.telegram_id,
            document=file,
            caption="Ваш FRP конфигурационный файл"
        )
        
        # Удаляем временный файл
        os.remove(filename)
        
        return {"status": "success"}