#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, time, json
import importlib

sys.path.append('conf/')

import configures 
import telegram_users 
CLIENT = telegram_users.clients
import advertisement
NOTICE = advertisement.notices

# apt install python3-pip
# pip install python-telegram-bot==21.6 --break-system-packages

import telegram  # type: ignore
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler # type: ignore

import language_uz
LANG = language_uz.LANGUAGES



# Функция, которая вызывается при нажатии на кнопку
async def button_click(update: telegram.Update, context):
    query = update.callback_query
    await query.answer()  # Обязательный метод для Telegram
    id = query.from_user.id
    name = '%s %s' % (query.from_user.first_name, query.from_user.last_name)
    name = name.replace('None', '')
    if len(name) < 3: name = LANG['unknown_user']
    button_name = query.data  # Получаем название кнопки
    if button_name == 'button_client': 
        await button_client(query, context)
    elif button_name == 'button_renter':
        pass
    else:
        lang_module = importlib.import_module(button_name)  # Импортируем модуль
        LANG = lang_module.LANGUAGES
        CLIENT[str(id)] = {"name": name, "time": time.strftime("%Y-%m-%d %H:%M:%S"), "lang": button_name[9:]}
        with open("conf/telegram_users.py", "w", encoding="utf-8") as file: file.write('clients = ' + json.dumps(CLIENT, indent=4))
        await choose_action(query, context)
    # await query.edit_message_text(LANG['bir_narsa'] + f" {button_name}")


async def user_register(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    # START 
    name = '%s %s' % (update.message.from_user.first_name, update.message.from_user.last_name)
    if CLIENT.get(str(update.message.from_user.id)):       # eski user, tanidim ??????????
        await choose_action(update, context)
    else: 
        # CLIENT[str(id)] = {'name': name, 'time': time.strftime("%d/%m/%Y, %H:%M:%S")}
        keyboard = [
            [
                telegram.InlineKeyboardButton(LANG['lang_uz'], callback_data='language_uz'),
                telegram.InlineKeyboardButton(LANG['lang_ru'], callback_data='language_ru'),
                telegram.InlineKeyboardButton(LANG['lang_en'], callback_data='language_en')
            ]
        ]
        buttons = telegram.InlineKeyboardMarkup(keyboard)
        msg = name + ', ' + LANG['choose_lang']
        await update.message.reply_text(msg, reply_markup=buttons)

async def show_message(update, msg, btn=None):
    try:
        await update.message.reply_text(msg, reply_markup=btn)
    except:
        await update.edit_message_text(msg, reply_markup=btn)


async def choose_action(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            telegram.InlineKeyboardButton(LANG['client'], callback_data='button_client'),
            telegram.InlineKeyboardButton(LANG['renter'], callback_data='button_renter')
        ]
    ]
    buttons = telegram.InlineKeyboardMarkup(keyboard)
    msg = LANG['bir_narsa']
    await show_message(update, msg, buttons)


async def button_client(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):

    msg = LANG['for_search']
    await show_message(update, msg)

# Обработчик для получения ответа от кнопок

async def handle_response(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text
    id = str(update.message.from_user.id)
    lang = CLIENT.get(id, {}).get("lang", "ru")
    
    if user_response == language_uz.LANGUAGES[LANG]["client"]:
        response_text = "Вы выбрали: Клиент"
    elif user_response == language_uz.LANGUAGES[LANG]["renter"]:
        response_text = "Вы выбрали: Арендатор"
    else:
        response_text = "Выберите корректный вариант: Клиент или Арендатор."

    await update.message.reply_text(response_text)

async def user_message(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text if update.message.text else "Сообщение содержит не текст."  
    response = f"Вы отправили сообщение: {msg}"
    await update.message.reply_text(response)


'''
PHOTO, PHONE, LOCATION, PRICE = range(4)

async def start_renter_conversation(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, отправьте фото дома.")
    return PHOTO

# Обработка фото
async def ask_phone(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохраняем фото
    photo = update.message.photo[-1]  # Берем последнюю фотографию (наибольшего разрешения)
    context.user_data['photo'] = photo  # Сохраняем фото в user_data для дальнейшего использования
    
    await update.message.reply_text("Теперь, пожалуйста, отправьте свой номер телефона.")
    return PHONE

# Обработка номера телефона
async def ask_location(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.message.text
    context.user_data['phone'] = phone_number  # Сохраняем номер телефона
    
    # Кнопка для отправки локации
    keyboard = [[telegram.KeyboardButton("Отправить локацию", request_location=True)]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text("Пожалуйста, отправьте свою локацию.", reply_markup=reply_markup)
    return LOCATION

# Обработка локации
async def ask_price(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    context.user_data['location'] = location  # Сохраняем локацию
    
    await update.message.reply_text("Укажите примерную цену аренды, например: 100-200$.")
    return PRICE

# Обработка цены
async def end_conversation(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    price = update.message.text
    context.user_data['price'] = price  # Сохраняем цену
    
    # Выводим собранную информацию
    msg = (
        "Спасибо! Вот ваши данные:\n"
        f"Фото: {context.user_data['photo'].file_id}\n"
        f"Телефон: {context.user_data['phone']}\n"
        f"Локация: {context.user_data['location'].latitude}, {context.user_data['location'].longitude}\n"
        f"Цена: {context.user_data['price']}"
    )
    await update.message.reply_text(msg)
    
    return ConversationHandler.END

# Обработчик выхода из диалога
async def cancel(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог был завершен.")
    return ConversationHandler.END

# Создаем обработчик разговора
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start_renter', start_renter_conversation)],
    states={
        PHOTO: [MessageHandler(filters.PHOTO, ask_phone)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)],
        LOCATION: [MessageHandler(filters.LOCATION, ask_price)],
        PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, end_conversation)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
'''

#################

bot = Application.builder().token(configures.RESEARCH_BOT_TOKEN).build()
# commands
bot.add_handler(CommandHandler("start", user_register))
bot.add_handler(CommandHandler("clients", button_client))
# inner buttons
bot.add_handler(CallbackQueryHandler(button_click))
# get user messages
bot.add_handler(MessageHandler(None, user_message))
bot.run_polling()





