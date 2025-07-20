import random
import string
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_subdomain_by_name

logger = logging.getLogger(__name__)

async def generate_unique_subdomain(db: AsyncSession, length=8) -> str:
    """Генерирует уникальный субдомен"""
    while True:
        subdomain = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        if not await get_subdomain_by_name(db, subdomain):
            return subdomain

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    return logger