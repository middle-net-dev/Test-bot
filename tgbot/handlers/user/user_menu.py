# - *- coding: utf- 8 - *-
import asyncio
from cgitb import text
from contextlib import suppress
import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted

from tgbot.data.config import BOT_DESCRIPTION
from tgbot.data.loader import dp
from tgbot.keyboards.inline_main import profile_open_inl
from tgbot.keyboards.inline_main import send_email_ini
from tgbot.keyboards.inline_main import send_bulk_email_ini
from tgbot.keyboards.inline_page import *
from tgbot.keyboards.inline_user import user_support_finl, products_open_finl, products_confirm_finl
from tgbot.keyboards.reply_main import menu_frep
from tgbot.services.api_sqlite import *
from tgbot.utils.const_functions import get_date, split_messages, get_unix, ded
from tgbot.utils.misc_functions import open_profile_user, upload_text, get_faq


# Открытие товаров
@dp.message_handler(text="🎁 Купить", state="*")
async def user_shop(message: Message, state: FSMContext):
    await state.finish()

    get_categories = get_all_categoriesx()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>🎁 Выберите нужный вам товар:</b>",
            reply_markup=products_item_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>🎁 Увы, товары в данное время отсутствуют.</b>")


# Открытие профиля
@dp.message_handler(text="👤 Профиль", state="*")
async def user_profile(message: Message, state: FSMContext):
    await state.finish()

    await message.answer(
        open_profile_user(message.from_user.id),
        reply_markup=profile_open_inl,
    )


# Проверка товаров в наличии
@dp.message_handler(text="🧮 Наличие товаров", state="*")
async def user_available(message: Message, state: FSMContext):
    await state.finish()

    get_categories = get_all_categoriesx()
    save_items = []

    for category in get_categories:
        get_positions = get_positionsx(category_id=category['category_id'])
        this_items = []

        if len(get_positions) >= 1:
            this_items = [f"<b>➖➖➖ {category['category_name']} ➖➖➖</b>"]

            for position in get_positions:
                get_items = get_itemsx(position_id=position['position_id'])

                if len(get_items) >= 1:
                    this_items.append(
                        f"{position['position_name']} | {position['position_price']}₽ | В наличии {len(get_items)} шт",
                    )

        if len(this_items) >= 2:
            save_items.append(this_items)

    if len(save_items) >= 1:
        send_items = ":^^^^^:".join(["\n".join(item) for item in save_items])

        if len(send_items) > 3500:
            split_items = split_messages(send_items.split("\n"), 40)

            for item in split_items:
                await message.answer("\n".join(item).replace(":^^^^^:", "\n\n"))
        else:
            await message.answer("\n\n".join(["\n".join(item) for item in save_items]))
    else:
        await message.answer("<b>🎁 Увы, товары в данное время отсутствуют.</b>")


# Открытие FAQ
@dp.message_handler(text=["ℹ FAQ", "/faq"], state="*")
async def user_faq(message: Message, state: FSMContext):
    await state.finish()

    send_message = get_settingsx()['misc_faq']
    if send_message == "None":
        send_message = ded(f"""
        ℹ Информация.
        ➖➖➖➖➖➖➖➖➖➖
        Подписка распространяется на все доступные сервисы в боте. 😉👍
        ➖➖➖➖➖➖➖➖➖➖
        🧾 Прайс цен на подписку:
        
        💥 17$ • <b>1 день</b>
        💥 45$ • <b>3 дня</b>
        💥 110$ • <b>7 дней</b>
        🔥 300$ • <b>30 дней</b>
                           
        ➖➖➖➖➖➖➖➖➖➖
        Интересует интеграция в вашего бота ?
        Пиши: <b><a href='https://t.me/thatwayyouknow'>noway</a></b>
        
        ➖➖➖➖➖➖➖➖➖➖
        ❗️ Нету нужного сервиса ? <b><a href='https://t.me/thatwayyouknow'>Пиши</a></b> - <b>добавим!</b> 
    """)

    await message.answer(get_faq(message.from_user.id, send_message), disable_web_page_preview=True)


#Открытие отправить письмо

@dp.message_handler(text=["📩 Отправить письмо", "/send"], state="*")
async def sendLetter(message: Message, state: FSMContext):
    await state.finish()

    get_user = get_userx(user_id=message.from_id)

    current_date = datetime.now()
    subscription_date_str = get_user['user_subscription'].split('.')[0]
    subscription = datetime.strptime(subscription_date_str, '%Y-%m-%d %H:%M:%S')

    time_difference = (subscription - current_date).total_seconds()

    if time_difference > 0:
        await message.answer(
            #open_profile_user(message.from_user.id),
            "<b>Выберите страну:</b>",
            reply_markup=send_email_ini,
        )
    else:
        await message.answer("<b>🎁 Увы, подписка не оплачена.</b>")


#Открытие массовая отправка

@dp.message_handler(text=["📩 Массовая отправка писем", "/send"], state="*")
async def sendLetter(message: Message, state: FSMContext):
    await state.finish()

    get_user = get_userx(user_id=message.from_id)

    current_date = datetime.now()
    subscription_date_str = get_user['user_subscription'].split('.')[0]
    subscription = datetime.strptime(subscription_date_str, '%Y-%m-%d %H:%M:%S')

    time_difference = (subscription - current_date).total_seconds()

    if time_difference > 0:
        await message.answer(
            #open_profile_user(message.from_user.id),
            "<b>Выберите сервис:</b>",
            reply_markup=send_bulk_email_ini,
        )
    else:
        await message.answer("<b>🎁 Увы, подписка не оплачена.</b>")


# Открытие сообщения с ссылкой на поддержку
@dp.message_handler(text=["☎ Поддержка", "/support"], state="*")
async def user_support(message: Message, state: FSMContext):
    await state.finish()

    get_settings = get_settingsx()

    if str(get_settings['misc_support']).isdigit():
        get_user = get_userx(user_id=get_settings['misc_support'])

        if len(get_user['user_login']) >= 1:
            return await message.answer(
                "<b>☎ Нажмите кнопку ниже для связи с Администратором.</b>",
                reply_markup=user_support_finl(get_user['user_login']),
            )
        else:
            update_settingsx(misc_support="None")

    await message.answer(
        ded(f"""
            ☎ Поддержка.
            ➖➖➖➖➖➖➖➖➖➖
            {BOT_DESCRIPTION}
        """),
        disable_web_page_preview=True,
    )


################################################################################################
# Просмотр истории покупок
@dp.callback_query_handler(text="user_history", state="*")
async def user_history(call: CallbackQuery, state: FSMContext):
    last_refills = last_refillsx(call.from_user.id, 5)

    if len(last_refills) >= 1:
        await call.answer("🎁 Последние 5 покупок")
        with suppress(MessageCantBeDeleted):
            await call.message.delete()

        for refills in last_refills:
            
            await call.message.answer(
                f"<b>🧾 Чек: <code>{refills['refill_receipt_id']}</code></b>\n"
                f"🎁 Тип оплаты: <code>{refills['refill_way']} | {refills['refill_amount']} {refills['refill_currency']}</code>\n"
                f"🕰 Дата покупки: <code>{refills['refill_date']}</code>\n"
            )


        await call.message.answer(open_profile_user(call.from_user.id), reply_markup=profile_open_inl)
    else:
        await call.answer("❗ Пополнения отсутствуют", True)


# Возвращение к профилю
@dp.callback_query_handler(text="user_profile", state="*")
async def user_profile_return(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        open_profile_user(call.from_user.id),
        reply_markup=profile_open_inl,
    )


################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>🎁 Выберите нужный вам товар:</b>",
        reply_markup=products_item_category_swipe_fp(remover),
    )


# Открытие категории для покупки
@dp.callback_query_handler(text_startswith="buy_category_open:", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_category = get_categoryx(category_id=category_id)
    get_positions = get_positionsx(category_id=category_id)

    if len(get_positions) >= 1:
        with suppress(MessageCantBeDeleted):
            await call.message.delete()

        await call.message.answer(
            f"<b>🎁 Текущая категория: <code>{get_category['category_name']}</code></b>",
            reply_markup=products_item_position_swipe_fp(remover, category_id),
        )
    else:
        if remover == "0":
            await call.message.edit_text("<b>🎁 Увы, товары в данное время отсутствуют.</b>")
            await call.answer("❗ Позиции были изменены или удалены")
        else:
            await call.answer(
                f"❕ Товары в категории {get_category['category_name']} отсутствуют",
                True,
                cache_time=5,
            )


# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_position_open:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    get_position = get_positionx(position_id=position_id)
    get_category = get_categoryx(category_id=category_id)
    get_items = get_itemsx(position_id=position_id)

    if get_position['position_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n📜 Описание:\n{get_position['position_description']}"

    send_msg = ded(f"""
        <b>🎁 Покупка товара:</b>
        ➖➖➖➖➖➖➖➖➖➖
        🏷 Название: <code>{get_position['position_name']}</code>
        🗃 Категория: <code>{get_category['category_name']}</code>
        💰 Стоимость: <code>{get_position['position_price']}₽</code>
        📦 Количество: <code>{len(get_items)}шт</code>
        {text_description}
    """)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    if len(get_position['position_photo']) >= 5:
        await call.message.answer_photo(
            get_position['position_photo'],
            send_msg,
            reply_markup=products_open_finl(position_id, category_id, remover),
        )
    else:
        await call.message.answer(
            send_msg,
            reply_markup=products_open_finl(position_id, category_id, remover),
        )


# Переключение страницы позиций для покупки
@dp.callback_query_handler(text_startswith="buy_position_swipe:", state="*")
async def user_purchase_position_next_page(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_category = get_categoryx(category_id=category_id)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()
    await call.message.answer(
        f"<b>🎁 Текущая категория: <code>{get_category['category_name']}</code></b>",
        reply_markup=products_item_position_swipe_fp(remover, category_id),
    )


########################################### ПОКУПКА ##########################################
# Выбор количества товаров для покупки
@dp.callback_query_handler(text_startswith="buy_item_open:", state="*")
async def user_purchase_select(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_position = get_positionx(position_id=position_id)
    get_items = get_itemsx(position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] / get_position['position_price'])
        if get_count > len(get_items): get_count = len(get_items)
    else:
        get_count = len(get_items)

    if int(get_user['user_balance']) >= int(get_position['position_price']):
        if get_count == 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.finish()

            with suppress(MessageCantBeDeleted):
                await call.message.delete()
            await call.message.answer(
                ded(f"""
                    <b>🎁 Вы действительно хотите купить товар(ы)?</b>
                    ➖➖➖➖➖➖➖➖➖➖
                    🎁 Товар: <code>{get_position['position_name']}</code>
                    📦 Количество: <code>1шт</code>
                    💰 Сумма к покупке: <code>{get_position['position_price']}₽</code>
                """),
                reply_markup=products_confirm_finl(position_id, 1),
            )
        elif get_count >= 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.set_state("here_item_count")

            with suppress(MessageCantBeDeleted):
                await call.message.delete()

            await call.message.answer(
                ded(f"""
                    <b>🎁 Введите количество товаров для покупки</b>
                    ▶ От <code>1</code> до <code>{get_count}</code>
                    ➖➖➖➖➖➖➖➖➖➖
                    🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>
                    💰 Ваш баланс: <code>{get_user['user_balance']}</code>
                """)
            )
        else:
            await call.answer("🎁 Товаров нет в наличии")
    else:
        await call.answer("❗ У вас недостаточно средств. Пополните баланс", True)


# Принятие количества товаров для покупки
@dp.message_handler(state="here_item_count")
async def user_purchase_select_count(message: Message, state: FSMContext):
    position_id = (await state.get_data())['here_cache_position_id']

    get_position = get_positionx(position_id=position_id)
    get_user = get_userx(user_id=message.from_user.id)
    get_items = get_itemsx(position_id=position_id)

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] / get_position['position_price'])

        if get_count > len(get_items):
            get_count = len(get_items)
    else:
        get_count = len(get_items)

    send_message = ded(f"""
        ➖➖➖➖➖➖➖➖➖➖
        🎁 Введите количество товаров для покупки
        ▶ От <code>1</code> до <code>{get_count}</code>
        ➖➖➖➖➖➖➖➖➖➖
        🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>
        💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>
    """)

    if message.text.isdigit():
        get_count = int(message.text)
        amount_pay = round(get_position['position_price'] * get_count, 2)

        if len(get_items) >= 1:
            if 1 <= get_count <= len(get_items):
                if int(get_user['user_balance']) >= amount_pay:
                    await state.finish()
                    await message.answer(
                        ded(f"""
                            <b>🎁 Вы действительно хотите купить товар(ы)?</b>
                            ➖➖➖➖➖➖➖➖➖➖
                            🎁 Товар: <code>{get_position['position_name']}</code>
                            📦 Количество: <code>{get_count}шт</code>
                            💰 Сумма к покупке: <code>{amount_pay}₽</code>
                        """),
                        reply_markup=products_confirm_finl(position_id, get_count),
                    )
                else:
                    await message.answer(f"<b>❌ Недостаточно средств на счете.</b>\n" + send_message)
            else:
                await message.answer(f"<b>❌ Неверное количество товаров.</b>\n" + send_message)
        else:
            await state.finish()
            await message.answer("<b>🎁 Товар который вы хотели купить, закончился</b>")
    else:
        await message.answer(f"<b>❌ Данные были введены неверно.</b>\n" + send_message)


# Подтверждение покупки товара
@dp.callback_query_handler(text_startswith="buy_item_confirm:", state="*")
async def user_purchase_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    get_count = int(call.data.split(":")[3])

    if get_action == "yes":
        await call.message.edit_text("<b>🔄 Ждите, товары подготавливаются</b>")

        get_position = get_positionx(position_id=position_id)
        get_items = get_itemsx(position_id=position_id)
        get_user = get_userx(user_id=call.from_user.id)

        amount_pay = round(get_position['position_price'] * get_count, 2)
        receipt, buy_time = get_unix(), get_date()

        if 1 <= int(get_count) <= len(get_items):
            if get_user['user_balance'] >= amount_pay:
                save_items, save_count, save_len = buy_itemx(get_items, get_count)

                if get_count != save_count:
                    amount_pay = round(get_position['position_price'] * save_count, 2)
                    get_count = save_count

                update_userx(get_user['user_id'], user_balance=round(get_user['user_balance'] - amount_pay, 2))
                add_purchasex(
                    get_user['user_id'], get_user['user_login'], get_user['user_name'], receipt, get_count,
                    amount_pay, get_position['position_price'], get_position['position_id'],
                    get_position['position_name'], "\n".join(save_items), buy_time, receipt,
                    get_user['user_balance'], round(get_user['user_balance'] - amount_pay, 2),
                )

                with suppress(MessageCantBeDeleted):
                    await call.message.delete()

                for item in split_messages(save_items, save_len):
                    await call.message.answer("\n\n".join(item), parse_mode="None")
                    await asyncio.sleep(0.3)

                await call.message.answer(
                    ded(f"""
                        <b>✅ Вы успешно купили товар(ы)</b>
                        ➖➖➖➖➖➖➖➖➖➖
                        🧾 Чек: <code>#{receipt}</code>
                        🎁 Товар: <code>{get_position['position_name']} | {get_count}шт | {amount_pay}₽</code>
                        🕰 Дата покупки: <code>{buy_time}</code>
                    """),
                    reply_markup=menu_frep(call.from_user.id),
                )
            else:
                await call.message.answer("<b>❗ На вашем счёте недостаточно средств</b>")
        else:
            await call.message.answer(
                "<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
                reply_markup=menu_frep(call.from_user.id),
            )
    else:
        get_categories = get_all_categoriesx()

        if len(get_categories) >= 1:
            await call.message.edit_text(
                "<b>🎁 Выберите нужный вам товар:</b>",
                reply_markup=products_item_category_swipe_fp(0),
            )
        else:
            await call.message.edit_text("<b>✅ Вы отменили покупку товаров.</b>")
