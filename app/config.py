import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Основные настройки
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")
    DATABASE_URL: str = "sqlite+aiosqlite:///app.db"
    
    # Платежные системы
    CRYPTOCLOUD_API_KEY: str = os.getenv("CRYPTOCLOUD_API_KEY")
    CRYPTOCLOUD_SHOP_ID: str = os.getenv("CRYPTOCLOUD_SHOP_ID")
    CRYPTOCLOUD_WEBHOOK_SECRET: str = os.getenv("CRYPTOCLOUD_WEBHOOK_SECRET")
    YOOKASSA_SHOP_ID: str = os.getenv("YOOKASSA_SHOP_ID")
    YOOKASSA_SECRET_KEY: str = os.getenv("YOOKASSA_SECRET_KEY")
    
    # FRP настройки
    FRP_SERVER_ADDR: str = os.getenv("FRP_SERVER_ADDR", "frp-server.com")
    FRP_SERVER_PORT: int = int(os.getenv("FRP_SERVER_PORT", 7000))
    FRP_DOMAIN: str = os.getenv("FRP_DOMAIN", "your-frp-domain.com")
    
    # Вебхуки
    WEBHOOK_PATH: str = "/webhook"
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET")
    BASE_WEBHOOK_URL: str = os.getenv("BASE_WEBHOOK_URL", "https://your-domain.com")
    
    # SSL для HTTPS
    SSL_CERT_PATH: str = os.getenv("SSL_CERT_PATH", "/path/to/cert.pem")
    SSL_KEY_PATH: str = os.getenv("SSL_KEY_PATH", "/path/to/key.pem")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()