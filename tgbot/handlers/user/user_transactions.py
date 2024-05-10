# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
import re
import datetime

import aiohttp
import asyncio
from tgbot.data.loader import dp
from tgbot.keyboards.inline_user import refill_bill_finl, refill_select_finl, choose_service_de_finl, choose_service_no_finl, choose_service_at_finl, choose_days_to_sub, get_sum_to_pay, get_pay_button, get_days_from_sum
from tgbot.services.api_qiwi import QiwiAPI
from tgbot.services.api_sqlite import update_userx, get_refillx, add_refillx, get_userx, update_data_to_sendx, get_data_go_sendx, add_sent_letter_infox
from tgbot.utils.const_functions import get_date, get_unix
from tgbot.utils.misc_functions import send_admins
from tgbot.utils.misc.bot_logging import bot_logger
from aiocryptopay import AioCryptoPay, Networks
import requests

min_input_qiwi = 5  # Минимальная сумма пополнения в рублях


# Выбор сервиса
@dp.callback_query_handler(text="paste_emails", state="*")
async def choose_service(call: CallbackQuery, state: FSMContext):

    await state.set_state("waiting_bulk_emails")
    # await message.answer("<b>Введите почты:</b>")    
    # get_services_de = choose_service_de_finl()
    # await call.message.edit_text("<b>Выберите сервис: </b>", reply_markup=get_services_de)
    await call.message.edit_text("<b>Введите почты: </b>")


# Выбор сервиса
@dp.callback_query_handler(text="choose_service_de", state="*")
async def choose_service(call: CallbackQuery, state: FSMContext):
    get_services_de = choose_service_de_finl()
    await call.message.edit_text("<b>Выберите сервис: </b>", reply_markup=get_services_de)

# Выбор сервиса
@dp.callback_query_handler(text="choose_service_no", state="*")
async def choose_service(call: CallbackQuery, state: FSMContext):
    get_services_no = choose_service_no_finl()
    await call.message.edit_text("<b>Выберите сервис: </b>", reply_markup=get_services_no)    

# Выбор сервиса
@dp.callback_query_handler(text="choose_service_at", state="*")
async def choose_service(call: CallbackQuery, state: FSMContext):
    get_services_at = choose_service_at_finl()
    await call.message.edit_text("<b>Выберите сервис: </b>", reply_markup=get_services_at)
   
# Отправить линку
@dp.callback_query_handler(text_startswith="enter_link", state="*")
async def enter_link(call: CallbackQuery, state: FSMContext):
    service = call.data.split(":")[1]
    country = call.data.split(":")[2]

    update_data_to_sendx(call.from_user.id, country = country, service = service)

    await state.set_state("waiting_link")
    await call.message.edit_text("<b>Введите ссылку</b>")

# Выбор способа пополнения
@dp.callback_query_handler(text="user_refill", state="*")
async def refill_way(call: CallbackQuery, state: FSMContext):
    get_kb = refill_select_finl()

    if get_kb is not None:
        await call.message.edit_text("<b>💰 Выберите способ пополнения</b>", reply_markup=get_kb)
    else:
        await call.answer("⛔ Пополнение временно недоступно", True)

# Выбор способа пополнения
@dp.callback_query_handler(text_startswith="refill_cryptobot", state="*")
async def refill_way_select(call: CallbackQuery, state: FSMContext):
    #get_way = call.data.split(":")[1]

    #await state.update_data(here_pay_way=get_way)
    get_subscription_types = choose_days_to_sub()
    await call.message.edit_text("<b>Выберите тип подписки: </b>", reply_markup=get_subscription_types)

    #await state.set_state("here_refill_amount")
    await state.set_state("here_refill_cryptobot")


# Выбор способа пополнения
@dp.callback_query_handler(text_startswith="type_refill_cryptobot", state="*")
async def refill_way_select(call: CallbackQuery, state: FSMContext):
    count_days = call.data.split(":")[1]

    sum_to_pay = get_sum_to_pay(int(count_days))

    crypto = AioCryptoPay(token='112943:AA0X3i5yXTduM2hyLs5f1DXcjphHssKRXpY', network=Networks.MAIN_NET)
    invoice = await crypto.create_invoice(asset='USDT', amount=sum_to_pay)

    reply = get_pay_button(invoice)

    #await state.update_data(here_pay_way=get_way)

    await state.finish()
    await call.message.edit_text(f"<b>К оплате {invoice.amount} </b>\n" 
                                    "Для оплаты перейдите по ссылке: ", reply_markup=reply)



# Выбор способа пополнения
@dp.callback_query_handler(text_startswith="refill_select", state="*")
async def refill_way_select(call: CallbackQuery, state: FSMContext):
    get_way = call.data.split(":")[1]

    await state.update_data(here_pay_way=get_way)

    await state.set_state("here_refill_amount")
    await call.message.edit_text("<b>💰 Введите сумму пополнения</b>")


###################################################################################
#################################### ВВОД ССЫЛКИ ###################################
# 
@dp.message_handler(state="waiting_link")
async def update_link(message: Message, state: FSMContext):
    if re.match(r'^(http|https)://', message.text):
        update_data_to_sendx(message.from_id, link = message.text)
        await state.set_state("waiting_email")
        await message.answer("<b>Введите email:</b>")             
    else:
        await message.answer("<b>❌ Введите корректную ссылку</b>")

###################################################################################
#################################### ВВОД ИМЕЙЛА ###################################
# 
@dp.message_handler(state="waiting_email")
async def update_email(message: Message, state: FSMContext):
    if re.match(r'^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$', message.text):         
        update_data_to_sendx(message.from_id, email = message.text)
        data = get_data_go_sendx(message.from_id)
        await state.finish()
        country = data[0]['country']
        service = data[0]['service']
        link = data[0]['link']
        email =  data[0]['email']
    
        await sent_success(message, state, country, service, email, link)
    else:
        await message.answer("<b>❌ Введите корректную почту</b>")

###################################################################################
#################################### ВВОД ПАЧКИ ###################################
# 
@dp.message_handler(state="waiting_bulk_emails")
async def update_email(message: Message, state: FSMContext): 
        update_data_to_sendx(message.from_id, email = message.text)
        data = get_data_go_sendx(message.from_id)
        await state.finish()
        email_str = data[0]['email']
        email_list = email_str.split('\n')
    
        await sent_bulk_success(message, state, email_list)
 


###################################################################################
#################################### ВВОД СУММЫ ###################################
# Принятие суммы для пополнения средств через QIWI
@dp.message_handler(state="here_refill_amount")
async def refill_get(message: Message, state: FSMContext):
    if message.text.isdigit():
        cache_message = await message.answer("<b>♻ Подождите, платёж генерируется...</b>")
        pay_amount = int(message.text)

        if min_input_qiwi <= pay_amount <= 300000:
            get_way = (await state.get_data())['here_pay_way']
            await state.finish()

            get_message, get_link, receipt = await (
                QiwiAPI(cache_message, pass_user=True)
            ).bill(pay_amount, get_way)

            if get_message:
                await cache_message.edit_text(get_message, reply_markup=refill_bill_finl(get_link, receipt, get_way))
        else:
            await cache_message.edit_text(
                f"<b>❌ Неверная сумма пополнения</b>\n"
                f"▶ Cумма не должна быть меньше <code>{min_input_qiwi}₽</code> и больше <code>300 000₽</code>\n"
                f"💰 Введите сумму для пополнения средств",
            )
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "💰 Введите сумму для пополнения средств")


###################################################################################
################################ ПРОВЕРКА ПЛАТЕЖЕЙ ################################
# Проверка оплаты криптобот
@dp.callback_query_handler(text_startswith="Pay:Cryptobot")
async def refill_check_form(call: CallbackQuery):
    invoice_id = call.data.split(":")[2]

    crypto = AioCryptoPay(token='112943:AA0X3i5yXTduM2hyLs5f1DXcjphHssKRXpY', network=Networks.MAIN_NET)
    invoices = await crypto.get_invoices(invoice_ids=invoice_id)

    if(invoices.count == 0):
        return await call.message.edit_text("Инвойс не найден")
    
    invoice = invoices[0]

    if invoice.status == "paid":
         await call.message.edit_text("<b>💰 Вы пополнили баланс на сумму <code>₽</code>. Удачи ❤\n"
            "🧾 Чек: <code>#</code></b>")
         #get_refill = get_refillx(refill_receipt=invoice)
         #if get_refill is None:
         await refill_success(call, invoice, "cryptobot")
         #else:
         #   await call.answer("❗ Ваше пополнение уже было зачислено.", True)
    elif invoice.status == "expired":
        await call.message.edit_text("<b>❌ Время оплаты вышло. Платёж был удалён.</b>")
    elif invoice.status == "active":
        await call.answer("❗ Платёж не был найден.\n"
                          "⌛ Попробуйте чуть позже.", True, cache_time=5)
    elif invoice.status == "rejected":
        await call.message.edit_text("<b>❌ Счёт был отклонён.</b>")


# Проверка оплаты через форму
@dp.callback_query_handler(text_startswith="Pay:Form")
async def refill_check_form(call: CallbackQuery):
    receipt = call.data.split(":")[2]

    pay_status, pay_amount = await (
        QiwiAPI(call, pass_user=True)
    ).check_form(receipt)

    if pay_status == "PAID":
        get_refill = get_refillx(refill_receipt=receipt)
        if get_refill is None:
            await refill_success(call, receipt, pay_amount, "Form")
        else:
            await call.answer("❗ Ваше пополнение уже было зачислено.", True)
    elif pay_status == "EXPIRED":
        await call.message.edit_text("<b>❌ Время оплаты вышло. Платёж был удалён.</b>")
    elif pay_status == "WAITING":
        await call.answer("❗ Платёж не был найден.\n"
                          "⌛ Попробуйте чуть позже.", True, cache_time=5)
    elif pay_status == "REJECTED":
        await call.message.edit_text("<b>❌ Счёт был отклонён.</b>")


# Проверка оплаты по переводу (по нику или номеру)
@dp.callback_query_handler(text_startswith=['Pay:Number', 'Pay:Nickname'])
async def refill_check_send(call: CallbackQuery):
    way_pay = call.data.split(":")[1]
    receipt = call.data.split(":")[2]

    pay_status, pay_amount = await (
        QiwiAPI(call, pass_user=True)
    ).check_send(receipt)

    if pay_status == 1:
        await call.answer("❗ Оплата была произведена не в рублях.", True, cache_time=5)
    elif pay_status == 2:
        await call.answer("❗ Платёж не был найден.\n"
                          "⌛ Попробуйте чуть позже.", True, cache_time=5)
    elif pay_status == 4:
        pass
    else:
        get_refill = get_refillx(refill_receipt=receipt)
        if get_refill is None:
            await refill_success(call, receipt, pay_amount, way_pay)
        else:
            await call.answer("❗ Ваше пополнение уже зачислено.", True, cache_time=60)


##########################################################################################
######################################### ПРОЧЕЕ #########################################
# Зачисление дней
async def refill_success(call: CallbackQuery, invoice, get_way):
    get_user = get_userx(user_id=call.from_user.id)

    add_refillx(get_user['user_id'], get_user['user_login'], get_user['user_name'], invoice.invoice_id,
                invoice.amount, invoice.asset, invoice.comment, get_way, get_date(), get_unix())

    current_date = datetime.now()
    subscription_date_str = get_user['user_subscription'].split('.')[0]
    subscription = datetime.strptime(subscription_date_str, '%Y-%m-%d %H:%M:%S')

    time_difference = (subscription - current_date).total_seconds()

    days_to_add = get_days_from_sum(invoice.amount)

    if(time_difference > 0):
        update_userx(
            call.from_user.id,
            user_subscription=subscription + datetime.timedelta(days_to_add),
            user_refill=get_user['user_refill'] + invoice.amount,
        )
    else:
        update_userx(
            call.from_user.id,
            user_subscription=current_date + datetime.timedelta(days_to_add),
            user_refill=get_user['user_refill'] + invoice.amount,
        )
        

    await call.message.edit_text(
        f"<b>💰 Вы пополнили баланс на сумму {invoice.amount}₽. Удачи ❤</b>\n"
    )

    await send_admins(
        f"👤 Пользователь: <b>@{get_user['user_login']}</b> | <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a> | <code>{get_user['user_id']}</code>\n"
        f"💰 Сумма пополнения: <code>{invoice.amount}$</code>\n"
    )
    


# Зачисление средств
#async def refill_success(call: CallbackQuery, receipt, amount, get_way):
#    get_user = get_userx(user_id=call.from_user.id)
#
#    add_refillx(get_user['user_id'], get_user['user_login'], get_user['user_name'], receipt,
#                amount, receipt, get_way, get_date(), get_unix())
#
#    update_userx(
#        call.from_user.id,
#        user_balance=get_user['user_balance'] + amount,
#        user_refill=get_user['user_refill'] + amount,
#    )
#
#    await call.message.edit_text(
#        f"<b>💰 Вы пополнили баланс на сумму <code>{amount}₽</code>. Удачи ❤\n"
#        f"🧾 Чек: <code>#{receipt}</code></b>",
#    )
#
#    await send_admins(
#        f"👤 Пользователь: <b>@{get_user['user_login']}</b> | <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a> | <code>{get_user['user_id']}</code>\n"
#        f"💰 Сумма пополнения: <code>{amount}₽</code>\n"
#        f"🧾 Чек: <code>#{receipt}</code>"
#    )

##########################################################################################
######################################### ПРОЧЕЕ #########################################
# Зачисление средств
async def sent_success(message: Message, state: FSMContext, country, service, email, link):
    url = f'https://noway-mailer.herokuapp.com/api/Sender{country}/{service}'
    params = {'email': email, 'link': link}

    msg =  await message.answer(
                f"📩 Подождите, идет отправка..."
            )
   
    # Отправка GET-запроса  
    response = requests.get(url, params=params)

    await msg.delete()

    if(response.status_code == 200):
        add_sent_letter_infox(message.from_id , country, service, email, link, get_date(), get_unix())
        
        await message.answer(
            f"✅ Письмо было успешно отправлено!"
        )
    else:
        bot_logger.exception(
            f"Exception: {response.reason}\n"
            f"Update: {response.status_code}"
        )

        await message.answer(
            f"❌ Ошибка"
        )

# async def sent_bulk_success(message: Message, state: FSMContext, email_list):
#     url = 'https://noway-mailer.herokuapp.com/api/Sender/Crypto'
#     #url = 'http://localhost:5216/api/Sender/Crypto'
    
#     timeout = aiohttp.ClientTimeout(total=600)

#     data = {"Emails": email_list}

#     msg = await message.answer(
#         f"📩 Подождите, идет отправка..."
#     )

#     try:
#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             async with session.post(url, json=data) as response:
#                 if response.status == 200:
#                     await message.answer(
#                         f"✅ Письмо было успешно отправлено!"
#                     )
#                 else:
#                     bot_logger.exception(
#                         f"Exception: {response.reason}\n"
#                         f"Update: {response.status_code}"
#                     )
                      
#                     await message.answer(
#                         f"❌ Ошибка"
#                     )
#     except asyncio.TimeoutError:
#         await message.answer(
#                         f"❌ По таймауту"
#                     )
#     except Exception as e:
#         await message.answer(
#                         f"❌ ОШибка"
#                     )
#     finally:
#         await msg.delete()


# Зачисление средств
# async def sent_bulk_success(message: Message, state: FSMContext, email_list):
#     url = f'https://noway-mailer.herokuapp.com/api/Sender/Crypto'
#     # url = f'http://localhost:5216/api/Sender/Crypto'
    
#     data = {"Emails": email_list}

#     msg =  await message.answer(
#                 f"📩 Подождите, идет отправка..."
#             )
   
#     # Отправка GET-запроса  
#     response = requests.post(url, json=data)

#     await msg.delete()

#     if(response.status_code == 200):
#         await message.answer(
#             f"✅ Письмо было успешно отправлено!"
#         )
#     else:
#         bot_logger.exception(
#             f"Exception: {response.reason}\n"
#             f"Update: {response.status_code}"
#         )

#         await message.answer(
#             f"❌ Ошибка"
#         )


# Зачисление средств
async def sent_bulk_success(message: Message, state: FSMContext, email_list):
    # url_base = 'https://noway-mailer.herokuapp.com/api/Sender/Crypto'
    url_base = 'http://localhost:5216/api/Sender/Crypto'

    msg = await message.answer(
        f"📩 Подождите, идет отправка..."
    )

    for email in email_list:
        data = {"Emails": [email]}

        # Отправка POST-запроса для каждого email
        response = requests.post(url_base, json=data)

        if response.status_code == 200:
            await message.answer(
                f"✅ Письмо для {email} было успешно отправлено!"
            )
        else:
            bot_logger.exception(
                f"Exception: {response.reason}\n"
                f"Update: {response.status_code}"
            )

            await message.answer(
                f"❌ Ошибка при отправке для {email}"
            )

    await msg.delete()