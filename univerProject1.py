#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, time, json
import importlib

sys.path.append('conf/')

import configures 
import telegram_users 
CLIENT = telegram_users.clients

# apt install python3-pip
# pip install python-telegram-bot==21.6 --break-system-packages

import telegram  # type: ignore
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler # type: ignore

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
    lang_module = importlib.import_module(button_name)  # Импортируем модуль
    LANG = lang_module.LANGUAGES
    CLIENT[str(id)] = {"name": name, "time": time.strftime("%Y-%m-%d %H:%M:%S"), "lang": button_name[9:]}
    with open("conf/telegram_users.py", "w", encoding="utf-8") as file: file.write('clients = ' + json.dumps(CLIENT, indent=4))
    await query.edit_message_text(LANG['bir_narsa'] + f" {button_name}")


async def user_register(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    name = '%s %s' % (update.message.from_user.first_name, update.message.from_user.last_name)
    buttons = None
    if CLIENT.get(str(update.message.from_user.id)):       # eski user, tanidim ??????????
        msg = name
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



bot = Application.builder().token(configures.RESEARCH_BOT_TOKEN).build()
bot.add_handler(CommandHandler("start", user_register))
bot.add_handler(CallbackQueryHandler(button_click))

# bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_response))
bot.run_polling()

