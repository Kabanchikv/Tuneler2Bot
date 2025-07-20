import requests
import uuid
import base64
from fastapi import HTTPException
from .config import settings

def create_yookassa_payment(amount: float, description: str, order_id: str, return_url: str) -> str:
    """Создает платеж в ЮKassa"""
    url = "https://api.yookassa.ru/v3/payments"
    headers = {
        "Idempotence-Key": str(uuid.uuid4()),
        "Content-Type": "application/json",
        "Authorization": f"Basic {base64.b64encode(f'{settings.YOOKASSA_SHOP_ID}:{settings.YOOKASSA_SECRET_KEY}'.encode()).decode()}"
    }
    payload = {
        "amount": {"value": amount, "currency": "RUB"},
        "confirmation": {"type": "redirect", "return_url": return_url},
        "description": description,
        "capture": True,
        "metadata": {"order_id": order_id}
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get('confirmation', {}).get('confirmation_url')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"YooKassa error: {str(e)}")

def verify_yookassa_webhook(data: dict) -> bool:
    """Проверяет вебхук от ЮKassa (базовая проверка)"""
    # В реальном приложении нужно проверять подпись
    return data.get('event') == 'payment.succeeded' and data.get('object', {}).get('paid') is True