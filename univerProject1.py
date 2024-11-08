#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import importlib

sys.path.append('conf/')

import configures # type: ignore

# apt install python3-pip
# pip install python-telegram-bot==21.6 --break-system-packages


import telegram  # type: ignore
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler # type: ignore

TELEGRAM_USER = {}

import language_uz
LANG = language_uz.LANGUAGES



# Функция, которая вызывается при нажатии на кнопку
async def button_click(update: telegram.Update, context):
    query = update.callback_query
    await query.answer()  # Обязательный метод для Telegram
    button_name = query.data  # Получаем название кнопки
    lang_module = importlib.import_module(button_name)  # Импортируем модуль
    LANG = lang_module.LANGUAGES
    await query.edit_message_text(LANG['bir_balo'] + f" {button_name}")


async def user_register(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            telegram.InlineKeyboardButton(LANG['lang_uz'], callback_data='language_uz'),
            telegram.InlineKeyboardButton(LANG['lang_ru'], callback_data='language_ru'),
            telegram.InlineKeyboardButton(LANG['lang_en'], callback_data='language_en')
        ]
    ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(LANG['choose_lang'], reply_markup=reply_markup)



bot = Application.builder().token(configures.RESEARCH_BOT_TOKEN).build()
bot.add_handler(CommandHandler("start", user_register))
bot.add_handler(CallbackQueryHandler(button_click))

# bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_response))
bot.run_polling()



exit()

bot = telegram.Bot(token=configures.RESEARCH_BOT_TOKEN)
updater = telegram.Updater(bot=bot, update_queue=my_queue)

updater.dispatcher.add_handler(CommandHandler('start', user_register))




exit()
#########################################################################################################
# Обработчик для выбора языка
async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split('_')[1]  # Получаем код языка (uz, ru, en)

    # Сохраняем выбранный язык для пользователя
    user_id = query.from_user.id
    user_language[user_id] = lang_code

    # Отображение следующего сообщения на выбранном языке
    text = LANGUAGES[lang_code]["select_role"]
    keyboard = [
        [
            telegram.InlineKeyboardButton(LANGUAGES[lang_code]["client"], callback_data='role_client'),
            InlineKeyboardButton(LANGUAGES[lang_code]["tenant"], callback_data='role_tenant')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# Обработчик для выбора роли (клиент или арендатор)
async def role_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang_code = user_language.get(user_id, 'en')  # Получаем выбранный язык, по умолчанию English

    # Сообщение для роли
    if query.data == 'role_client':
        text = f"{LANGUAGES[lang_code]['client']} выбран."
    elif query.data == 'role_tenant':
        text = f"{LANGUAGES[lang_code]['tenant']} выбран."
    else:
        text = "Выбор не распознан."

    await query.edit_message_text(text=text)

'''
# Команда /start
async def start(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	btn = telegram.ReplyKeyboardMarkup([["🇺🇿 UZB", "🇷🇺 Rus"]], resize_keyboard=True)
	name = '%s %s! %s' % (update.message.from_user.first_name, update.message.from_user.last_name, update.message.from_user.id)
	await update.message.reply_text("Tilni tanlang, %s" % name, reply_markup=btn)

# Обработка сообщений
async def echo(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	user_message = update.message.text
	await update.message.reply_text(f"Эхо: {user_message}")
'''

def run_bot():
	app = Application.builder().token(configures.RESEARCH_BOT_TOKEN).build()

	app.add_handler(CommandHandler("start", start))
	app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

	app.run_polling()

if __name__ == "__main__":
	run_bot()




exit()

from telegram import Bot
from telegram.ext import Updater
#, CallbackContext, CommandHandler, MessageHandler, filters



def user_register(answer, context):
	s = 'Assalomu alaykum, %s %s. BOTdan foydalanish uchun telefon raqamingizni yuboring.'
	s = s % (answer.message.from_user.first_name, answer.message.from_user.last_name)
	contact_keyboard = telegram.KeyboardButton(text="Telefon raqamini yuborish", request_contact=True)
	reply_markup = telegram.ReplyKeyboardMarkup([[contact_keyboard]])
	answer.message.reply_text(s, reply_markup=reply_markup)


# HOME_BTN = telegram.ReplyKeyboardMarkup([[languages.LANG['client'], languages.LANG['renter']]], resize_keyboard=True)
# HTML = telegram.ParseMode.HTML


# print(languages.LANG.get('hello', 'Hello!'))
print(configures.RESEARCH_BOT_TOKEN)
my_queue = queue.Queue()

bot = Bot(token=configures.RESEARCH_BOT_TOKEN)
updater = Updater(bot=bot, update_queue=my_queue)

updater.dispatcher.add_handler(CommandHandler('start', user_register))



