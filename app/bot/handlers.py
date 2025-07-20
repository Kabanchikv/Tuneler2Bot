from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from .keyboards import (
    get_main_keyboard,
    get_payment_methods_keyboard,
    get_tariffs_keyboard,
    get_admin_keyboard
)
from .states import SubscriptionStates, AdminStates
from app.database import async_session
from app.crud import (
    get_user_by_telegram_id,
    create_user,
    get_active_subscription,
    get_active_tariffs,
    create_subscription,
    update_user
)
from app.payments.cryptocloud import create_cryptocloud_payment
from app.payments.yookassa import create_yookassa_payment
from app.frp.utils import generate_unique_subdomain
import uuid
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("start"))
async def start(message: Message):
    async with async_session() as db:
        user = await get_user_by_telegram_id(db, message.from_user.id)
        if not user:
            user = await create_user(db, {
                "telegram_id": message.from_user.id,
                "username": message.from_user.username,
                "full_name": message.from_user.full_name
            })
    
    await message.answer(
        "🤖 Добро пожаловать! Этот бот предоставляет доступ к FRP серверам.\n"
        "Вы можете приобрести подписку и получить свой собственный субдомен.",
        reply_markup=get_main_keyboard(user.is_admin if user else False)
    )

@router.message(F.text == "🔄 Статус подписки")
async def subscription_status(message: Message):
    async with async_session() as db:
        subscription = await get_active_subscription(db, message.from_user.id)
        
        if subscription:
            await message.answer(
                f"📝 Ваш тариф: {subscription.tariff.name}\n"
                f"💵 Стоимость: {subscription.tariff.price}₽\n"
                f"⏳ Действует до: {subscription.end_date.strftime('%d.%m.%Y %H:%M')}\n"
                f"🌐 Ваш субдомен: {subscription.subdomain}.frp.example.com"
            )
        else:
            await message.answer("❌ У вас нет активной подписки.")

@router.message(F.text == "💳 Купить подписку")
async def buy_subscription(message: Message, state: FSMContext):
    async with async_session() as db:
        tariffs = await get_active_tariffs(db)
    
    if not tariffs:
        return await message.answer("😢 В данный момент нет доступных тарифов")
    
    await message.answer("Выберите тарифный план:", reply_markup=get_tariffs_keyboard(tariffs))
    await state.set_state(SubscriptionStates.CHOOSING_TARIFF)

@router.callback_query(F.data.startswith("tariff_"))
async def process_tariff(callback: CallbackQuery, state: FSMContext):
    tariff_id = int(callback.data.split("_")[1])
    await state.update_data(tariff_id=tariff_id)
    await callback.message.answer("Выберите платежную систему:", reply_markup=get_payment_methods_keyboard())
    await state.set_state(SubscriptionStates.CHOOSING_PAYMENT)

@router.callback_query(F.data.in_(["cryptocloud", "yookassa"]))
async def process_payment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tariff_id = data['tariff_id']
    user_id = callback.from_user.id
    
    async with async_session() as db:
        # Получаем тариф
        tariff = await get_tariff(db, tariff_id)
        if not tariff:
            return await callback.message.answer("❌ Тариф не найден")
        
        # Генерируем уникальный субдомен
        subdomain = await generate_unique_subdomain(db)
        
        # Создаем подписку (пока не активную)
        payment_id = str(uuid.uuid4())
        subscription = await create_subscription(db, {
            "user_id": user_id,
            "tariff_id": tariff_id,
            "subdomain": subdomain,
            "payment_id": payment_id
        })
        
        if not subscription:
            return await callback.message.answer("❌ Ошибка при создании подписки")
        
        # Создаем платеж
        payment_url = None
        if callback.data == "cryptocloud":
            payment_url = create_cryptocloud_payment(tariff.price, payment_id)
        elif callback.data == "yookassa":
            payment_url = create_yookassa_payment(
                tariff.price,
                f"Подписка {tariff.name}",
                payment_id,
                "https://t.me/your_bot"
            )
        
        if payment_url:
            await callback.message.answer(
                f"💸 Для оплаты подписки перейдите по ссылке: [Оплатить]({payment_url})",
                parse_mode="Markdown"
            )
        else:
            await callback.message.answer("❌ Ошибка при создании платежа")
    
    await state.clear()

@router.message(F.text == "👑 Админ-панель")
async def admin_panel(message: Message):
    async with async_session() as db:
        user = await get_user_by_telegram_id(db, message.from_user.id)
        if not user or not user.is_admin:
            return await message.answer("❌ У вас нет прав доступа")
    
    await message.answer("Админ-панель:", reply_markup=get_admin_keyboard())

@router.message(F.text == "📊 Управление тарифами")
async def manage_tariffs(message: Message):
    async with async_session() as db:
        user = await get_user_by_telegram_id(db, message.from_user.id)
        if not user or not user.is_admin:
            return
        
        tariffs = await get_active_tariffs(db)
        response = "📊 Список активных тарифов:\n\n"
        for tariff in tariffs:
            response += f"• {tariff.name} - {tariff.price}₽ ({tariff.duration_days} дней)\n"
        
        await message.answer(response)

@router.message(F.text == "⬅️ Назад в меню")
async def back_to_main_menu(message: Message):
    async with async_session() as db:
        user = await get_user_by_telegram_id(db, message.from_user.id)
    
    await message.answer("Главное меню:", reply_markup=get_main_keyboard(user.is_admin if user else False))

@router.message(F.text)
async def admin_password(message: Message):
    """Обработка специального сообщения для получения прав администратора"""
    from app.config import settings
    
    if message.text == settings.ADMIN_PASSWORD:
        async with async_session() as db:
            user = await get_user_by_telegram_id(db, message.from_user.id)
            if user:
                await update_user(db, user.id, {"is_admin": True})
                await message.answer("✅ Вы получили права администратора!", reply_markup=get_main_keyboard(True))