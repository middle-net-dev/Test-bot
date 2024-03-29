# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from tgbot.data.config import get_admins


# Кнопки главного меню
def menu_frep(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row("📩 Отправить письмо", "👤 Профиль")
    keyboard.row("📩 Массовая отправка писем")
    keyboard.row("☎ Поддержка", "ℹ FAQ")

    if user_id in get_admins():
        keyboard.row("📊 Статистика", "⚙ Настройки")
        keyboard.row("🔆 Общие функции", "🔑 Платежные системы")

    return keyboard


# Кнопки платежных систем
def payments_frep():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    # keyboard.row("🥝 Изменить QIWI 🖍", "🥝 Проверить QIWI ♻", "🥝 Баланс QIWI 👁")
    keyboard.row("🤖 Неоплаченные счета Cryptobot ♻", "🤖 Баланс Cryptobot 👁")
    keyboard.row("🔙 Главное меню", "🖲 Способы пополнений")

    return keyboard


# Кнопки общих функций
def functions_frep(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row("👤 Поиск профиля 🔍", "📢 Рассылка", "🧾 Поиск чеков 🔍")
    keyboard.row("🔙 Главное меню")

    return keyboard


# Кнопки настроек
def settings_frep():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row("🖍 Изменить данные", "🕹 Выключатели")
    keyboard.row("🔙 Главное меню")

    return keyboard


# Кнопки изменения товаров
def items_frep():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row("🎁 Добавить товары ➕", "🎁 Удалить товары 🖍", "🎁 Удалить все товары ❌")
    keyboard.row("📁 Создать позицию ➕", "📁 Изменить позицию 🖍", "📁 Удалить все позиции ❌")
    keyboard.row("🗃 Создать категорию ➕", "🗃 Изменить категорию 🖍", "🗃 Удалить все категории ❌")
    keyboard.row("🔙 Главное меню")

    return keyboard


# Завершение загрузки товаров
finish_load_rep = ReplyKeyboardMarkup(resize_keyboard=True)
finish_load_rep.row("📥 Закончить загрузку товаров")
