# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.services.api_sqlite import get_paymentx


# Выбор сервиса Германия
def choose_service_de_finl():
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🇩🇪 Ebay Kleinanzeigen", callback_data="enter_link:ebay:Germany"),
        InlineKeyboardButton("🇩🇪 Shpock", callback_data="enter_link:shpock:Germany"),
    ).add(InlineKeyboardButton("🔙 Вернуться", callback_data="user_profile"))

    return keyboard

# Выбор сервиса Австрия
def choose_service_at_finl():
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🇦🇹 Shpock", callback_data="enter_link:shpock:Austria"),
    ).add(InlineKeyboardButton("🔙 Вернуться", callback_data="user_profile"))

    return keyboard

# Выбор сервиса
def choose_days_to_sub():
    keyboard = InlineKeyboardMarkup(
    ).add(InlineKeyboardButton("1 день", callback_data="type_refill_cryptobot:1"),
    InlineKeyboardButton("3 дня", callback_data="type_refill_cryptobot:3"),
    ).add(InlineKeyboardButton("7 дней", callback_data="type_refill_cryptobot:7"), 
    InlineKeyboardButton("30 дней", callback_data="type_refill_cryptobot:30")).add(InlineKeyboardButton("🔙 Вернуться", callback_data="user_profile"))

    return keyboard

# Сумма к оплате cryptobot
def get_sum_to_pay(days):
    payment_schedule = {
        1: 0.1,
        3: 0.13,
        7: 0.17,
        30: 0.2
    }
    
    return payment_schedule.get(days, None)

# Количество дней исходя из 
def get_days_from_sum(amount):
    payment_schedule = {
        0.1 : 1,
        0.13 : 3,
        0.17 : 7,
        0.2 : 30
    }
    
    return payment_schedule.get(amount, None)

# Выбор способов пополнения
def refill_select_finl():
    keyboard = InlineKeyboardMarkup()

    get_payments = get_paymentx()
    active_kb = []

    active_kb.append(InlineKeyboardButton("🤖 Cryptobot", callback_data="refill_cryptobot"))

    if get_payments['way_form'] == "True":
        active_kb.append(InlineKeyboardButton("📋 QIWI форма", callback_data="refill_select:Form"))
    if get_payments['way_number'] == "True":
        active_kb.append(InlineKeyboardButton("📞 QIWI номер", callback_data="refill_select:Number"))
    if get_payments['way_nickname'] == "True":
        active_kb.append(InlineKeyboardButton("Ⓜ QIWI никнейм", callback_data="refill_select:Nickname"))

    if len(active_kb) == 3:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2])
    elif len(active_kb) == 2:
        keyboard.add(active_kb[0], active_kb[1])
    elif len(active_kb) == 1:
        keyboard.add(active_kb[0])
    else:
        keyboard = None

    if len(active_kb) >= 1:
        keyboard.add(InlineKeyboardButton("🔙 Вернуться", callback_data="user_profile"))

    return keyboard

def get_pay_button(invoice):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("🌀 Перейти к оплате", url=invoice.pay_url)
    ).add(
        InlineKeyboardButton("🔄 Проверить оплату", callback_data=f"Pay:Cryptobot:{invoice.invoice_id}")
    )
    return keyboard


# Проверка киви платежа
def refill_bill_finl(send_requests, get_receipt, get_way):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("🌀 Перейти к оплате", url=send_requests)
    ).add(
        InlineKeyboardButton("🔄 Проверить оплату", callback_data=f"Pay:{get_way}:{get_receipt}")
    )

    return keyboard


# Кнопки при открытии самого товара
def products_open_finl(position_id, category_id, remover):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("💰 Купить товар", callback_data=f"buy_item_open:{position_id}:{remover}")
    ).add(
        InlineKeyboardButton("🔙 Вернуться", callback_data=f"buy_category_open:{category_id}:{remover}")
    )

    return keyboard


# Подтверждение покупки товара
def products_confirm_finl(position_id, get_count):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"buy_item_confirm:yes:{position_id}:{get_count}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"buy_item_confirm:not:{position_id}:{get_count}")
    )

    return keyboard


# Ссылка на поддержку
def user_support_finl(user_name):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("💌 Написать в поддержку", url=f"https://t.me/{user_name}"),
    )

    return keyboard
