import requests
import uuid
import hmac
import hashlib
import json
from fastapi import HTTPException
from .config import settings

def create_cryptocloud_payment(amount: float, order_id: str, currency: str = "RUB") -> str:
    """Создает платеж в CryptoCloud"""
    url = "https://api.cryptocloud.plus/v1/invoice/create"
    headers = {"Authorization": f"Token {settings.CRYPTOCLOUD_API_KEY}"}
    payload = {
        "shop_id": settings.CRYPTOCLOUD_SHOP_ID,
        "amount": amount,
        "currency": currency,
        "order_id": order_id
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get('pay_url')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CryptoCloud error: {str(e)}")

def verify_cryptocloud_webhook(data: dict, signature: str) -> bool:
    """Проверяет подпись вебхука от CryptoCloud"""
    sorted_data = dict(sorted(data.items()))
    message = json.dumps(sorted_data, separators=(',', ':'))
    secret = settings.CRYPTOCLOUD_WEBHOOK_SECRET.encode()
    generated_signature = hmac.new(secret, message.encode(), hashlib.sha256).hexdigest()
    return generated_signature == signature