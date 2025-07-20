from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import UserUpdate, TariffCreate, TariffUpdate
from .service import (
    get_users,
    update_user_role,
    create_tariff,
    get_tariffs,
    update_tariff,
    delete_tariff
)

router = APIRouter(tags=["admin"])

@router.get("/users")
async def admin_get_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

@router.patch("/users/{user_id}/role")
async def admin_update_user_role(
    user_id: int, 
    role_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await update_user_role(db, user_id, role_data.is_admin)

@router.post("/tariffs")
async def admin_create_tariff(
    tariff_data: TariffCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_tariff(db, tariff_data)

@router.get("/tariffs")
async def admin_get_tariffs(db: AsyncSession = Depends(get_db)):
    return await get_tariffs(db)

@router.patch("/tariffs/{tariff_id}")
async def admin_update_tariff(
    tariff_id: int,
    tariff_data: TariffUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await update_tariff(db, tariff_id, tariff_data)

@router.delete("/tariffs/{tariff_id}")
async def admin_delete_tariff(
    tariff_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await delete_tariff(db, tariff_id)