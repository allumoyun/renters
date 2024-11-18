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
        await button_renter(query, context)
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
        await update.edit_message_text(msg, reply_markup=btn)
    except:
        await update.message.reply_text(msg, reply_markup=btn)


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

    msg01 = LANG['for_search']
    await show_message(update, msg01)


async def button_renter(query: telegram.Update, context: ContextTypes.DEFAULT_TYPE, question="address"):
    try: id = str(query.from_user.id)
    except: id = str(query.message.from_user.id)
    elm = {"question": question}
    if NOTICE.get(id): 
        if question == "address": NOTICE[id].append(elm)
    else: NOTICE[id] = [elm]
    print('BUTTON RENTER: ', NOTICE)
    await show_message(query, LANG['enter_' + question])

# Обработчик для получения ответа от кнопок


async def user_message(query: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try: id = str(query.from_user.id)
    except: id = str(query.message.from_user.id)
    # elif NOTICE[id][len(NOTICE[id])-1]["question"] == "photos":
    #     NOTICE[id][len(NOTICE[id])-1]["photos"] = query.message.photo
    if NOTICE.get(id) and query.message.location and NOTICE[id][len(NOTICE[id])-1]["question"] == 'location':
        latitude = query.message.location.latitude
        longitude = query.message.location.longitude
        NOTICE[id][len(NOTICE[id])-1]["location"] = f"{latitude};{longitude}"
        NOTICE[id][len(NOTICE[id])-1]["question"] = "cost"
    elif NOTICE.get(id) and query.message.contact:
        if NOTICE[id][len(NOTICE[id])-1]["question"] == 'contact':
            NOTICE[id][len(NOTICE[id])-1]["contact"] = query.message.contact.phone_number
            NOTICE[id][len(NOTICE[id])-1]["question"] = 'ready'
            with open("conf/advertisement.py", "w", encoding="utf-8") as file: 
                file.write('notices = ' + json.dumps(NOTICE, indent=4))
    elif NOTICE.get(id) and query.message.text: 
        if NOTICE[id][len(NOTICE[id])-1]["question"] == 'address':
            NOTICE[id][len(NOTICE[id])-1]["address"] = query.message.text
            NOTICE[id][len(NOTICE[id])-1]["question"] = "description"
        elif NOTICE[id][len(NOTICE[id])-1]["question"] == 'description':
            NOTICE[id][len(NOTICE[id])-1]["description"] = query.message.text
            NOTICE[id][len(NOTICE[id])-1]["question"] = "location"
        elif NOTICE[id][len(NOTICE[id])-1]["question"] == 'cost':
            if query.message.text.isdigit():
                NOTICE[id][len(NOTICE[id])-1]["cost"] = query.message.text
                NOTICE[id][len(NOTICE[id])-1]["question"] = "contact"                
    print('MESSAGE: ', NOTICE)
    keyboard = [ [telegram.KeyboardButton(LANG['contact_button'], request_contact=True)] ]
    if NOTICE[id][len(NOTICE[id])-1]["question"] == "contact":
        btn_phone = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    else: btn_phone = telegram.ReplyKeyboardRemove()
    await show_message(query, LANG['enter_' + NOTICE[id][len(NOTICE[id])-1]["question"]], btn_phone)






#################

bot = Application.builder().token(configures.RESEARCH_BOT_TOKEN).build()
# commands
bot.add_handler(CommandHandler("start", user_register))
bot.add_handler(CommandHandler("clients", button_client))
bot.add_handler(CommandHandler("renter", button_renter))
# inner buttons
bot.add_handler(CallbackQueryHandler(button_click))
# get user messages
bot.add_handler(MessageHandler(None, user_message))
bot.run_polling()





