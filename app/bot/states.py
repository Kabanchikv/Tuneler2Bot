from aiogram.fsm.state import State, StatesGroup

class SubscriptionStates(StatesGroup):
    CHOOSING_TARIFF = State()
    CHOOSING_PAYMENT = State()

class AdminStates(StatesGroup):
    ADDING_TARIFF = State()
    EDITING_TARIFF = State()
    MANAGING_USERS = State()