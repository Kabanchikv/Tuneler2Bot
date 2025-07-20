from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard(is_admin: bool = False):
    """Клавиатура главного меню"""
    keyboard = [
        [KeyboardButton(text="🔄 Статус подписки")],
        [KeyboardButton(text="💳 Купить подписку")]
    ]
    
    if is_admin:
        keyboard.append([KeyboardButton(text="👑 Админ-панель")])
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_payment_methods_keyboard():
    """Клавиатура выбора платежной системы"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="CryptoCloud", callback_data="cryptocloud")],
        [InlineKeyboardButton(text="ЮKassa", callback_data="yookassa")]
    ])

def get_tariffs_keyboard(tariffs):
    """Клавиатура выбора тарифного плана"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for tariff in tariffs:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"{tariff.name} - {tariff.price}₽",
                callback_data=f"tariff_{tariff.id}"
            )
        ])
    return keyboard

def get_admin_keyboard():
    """Клавиатура админ-панели"""
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="👥 Управление пользователями")],
        [KeyboardButton(text="📊 Управление тарифами")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ], resize_keyboard=True)