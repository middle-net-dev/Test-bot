# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Рассылка
mail_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("✅ Отправить", callback_data="confirm_mail:yes"),
    InlineKeyboardButton("❌ Отменить", callback_data="confirm_mail:not")
)

# Кнопки при поиске профиля через админ-меню
profile_open_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("💰 Пополнить", callback_data="user_refill"),
    InlineKeyboardButton("🧾  История пополнений", callback_data="user_history")
)

# Кнопки при нажатии отправить письмо
send_email_ini = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("🇩🇪 Германия", callback_data="choose_service_de"),
    InlineKeyboardButton("🇦🇹 Австрия", callback_data="choose_service_at")
)

# Удаление сообщения
close_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Закрыть", callback_data="close_this"),
)

######################################## ТОВАРЫ ########################################
# Удаление категорий
category_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все", callback_data="confirm_remove_category:yes"),
    InlineKeyboardButton("✅ Нет, отменить", callback_data="confirm_remove_category:not")
)

# Удаление позиций
position_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все", callback_data="confirm_remove_position:yes"),
    InlineKeyboardButton("✅ Нет, отменить", callback_data="confirm_remove_position:not")
)

# Удаление товаров
item_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все", callback_data="confirm_remove_item:yes"),
    InlineKeyboardButton("✅ Нет, отменить", callback_data="confirm_remove_item:not")
)
