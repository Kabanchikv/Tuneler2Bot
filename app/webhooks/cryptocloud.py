from fastapi import APIRouter, Request, HTTPException
from app.database import async_session
from app.crud import get_subscription_by_payment_id, update_subscription
from app.frp.utils import generate_frp_config, save_toml_file
from app.bot.core import bot
from aiogram.types import FSInputFile
from .config import settings
import os

router = APIRouter()

@router.post("/cryptocloud")
async def cryptocloud_webhook(request: Request):
    data = await request.json()
    signature = request.headers.get("Signature")
    
    # Проверка подписи
    if not verify_cryptocloud_webhook(data, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Обработка успешного платежа
    if data.get('status') == 'paid':
        order_id = data['order_id']
        
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
    
    return {"status": "ignored"}