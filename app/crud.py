from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from . import models
import logging

logger = logging.getLogger(__name__)

# User CRUD
async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int):
    result = await db.execute(
        select(models.User)
        .where(models.User.telegram_id == telegram_id)
    )
    return result.scalars().first()

async def create_user(db: AsyncSession, user_data: dict):
    user = models.User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(db: AsyncSession, user_id: int, user_data: dict):
    await db.execute(
        update(models.User)
        .where(models.User.id == user_id)
        .values(**user_data)
    )
    await db.commit()
    return await get_user_by_id(db, user_id)

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user_id)
    )
    return result.scalars().first()

# Tariff CRUD
async def get_tariff(db: AsyncSession, tariff_id: int):
    result = await db.execute(
        select(models.Tariff)
        .where(models.Tariff.id == tariff_id)
    )
    return result.scalars().first()

async def get_active_tariffs(db: AsyncSession):
    result = await db.execute(
        select(models.Tariff)
        .where(models.Tariff.is_active == True)
    )
    return result.scalars().all()

async def create_tariff(db: AsyncSession, tariff_data: dict):
    tariff = models.Tariff(**tariff_data)
    db.add(tariff)
    await db.commit()
    await db.refresh(tariff)
    return tariff

async def update_tariff(db: AsyncSession, tariff_id: int, tariff_data: dict):
    await db.execute(
        update(models.Tariff)
        .where(models.Tariff.id == tariff_id)
        .values(**tariff_data)
    )
    await db.commit()
    return await get_tariff(db, tariff_id)

async def delete_tariff(db: AsyncSession, tariff_id: int):
    await db.execute(
        delete(models.Tariff)
        .where(models.Tariff.id == tariff_id)
    )
    await db.commit()

# Subscription CRUD
async def create_subscription(db: AsyncSession, subscription_data: dict):
    # Получаем тариф для расчета даты окончания
    tariff = await get_tariff(db, subscription_data["tariff_id"])
    if not tariff:
        return None
    
    end_date = datetime.utcnow() + timedelta(days=tariff.duration_days)
    subscription = models.Subscription(
        **subscription_data,
        end_date=end_date
    )
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription

async def get_active_subscription(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Subscription)
        .where(
            models.Subscription.user_id == user_id,
            models.Subscription.is_active == True
        )
        .options(selectinload(models.Subscription.tariff))
    )
    return result.scalars().first()

async def get_subscription_by_payment_id(db: AsyncSession, payment_id: str):
    result = await db.execute(
        select(models.Subscription)
        .where(models.Subscription.payment_id == payment_id)
        .options(selectinload(models.Subscription.user))
    )
    return result.scalars().first()

async def update_subscription(db: AsyncSession, subscription_id: int, update_data: dict):
    await db.execute(
        update(models.Subscription)
        .where(models.Subscription.id == subscription_id)
        .values(**update_data)
    )
    await db.commit()

async def get_expired_subscriptions(db: AsyncSession):
    result = await db.execute(
        select(models.Subscription)
        .where(
            models.Subscription.end_date < datetime.utcnow(),
            models.Subscription.is_active == True
        )
    )
    return result.scalars().all()

async def deactivate_subscription(db: AsyncSession, subscription_id: int):
    await update_subscription(db, subscription_id, {"is_active": False})

async def get_subdomain_by_name(db: AsyncSession, subdomain: str):
    result = await db.execute(
        select(models.Subscription)
        .where(models.Subscription.subdomain == subdomain)
    )
    return result.scalars().first()