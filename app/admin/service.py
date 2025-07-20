from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.schemas import UserUpdate, TariffCreate, TariffUpdate

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получение списка пользователей"""
    return await crud.get_users(db, skip, limit)

async def update_user_role(db: AsyncSession, user_id: int, is_admin: bool):
    """Обновление роли пользователя"""
    return await crud.update_user(db, user_id, {"is_admin": is_admin})

async def create_tariff(db: AsyncSession, tariff_data: TariffCreate):
    """Создание нового тарифного плана"""
    return await crud.create_tariff(db, tariff_data.dict())

async def get_tariffs(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получение списка тарифов"""
    return await crud.get_tariffs(db, skip, limit)

async def update_tariff(db: AsyncSession, tariff_id: int, tariff_data: TariffUpdate):
    """Обновление тарифного плана"""
    return await crud.update_tariff(db, tariff_id, tariff_data.dict(exclude_unset=True))

async def delete_tariff(db: AsyncSession, tariff_id: int):
    """Удаление тарифного плана"""
    return await crud.delete_tariff(db, tariff_id)