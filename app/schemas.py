from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    telegram_id: int
    username: str | None = None
    full_name: str

class UserUpdate(BaseModel):
    is_admin: bool | None = None

class TariffCreate(BaseModel):
    name: str
    description: str
    price: float
    duration_days: int

class TariffUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    duration_days: int | None = None
    is_active: bool | None = None

class SubscriptionCreate(BaseModel):
    user_id: int
    tariff_id: int
    subdomain: str

class SubscriptionOut(BaseModel):
    id: int
    user_id: int
    tariff_id: int
    start_date: datetime
    end_date: datetime
    subdomain: str
    is_active: bool