import telebot
from telebot import types, TeleBot
from telebot.types import InlineKeyboardButton
import logging
from telegram_bot_pagination import InlineKeyboardPaginator
from data import smm,...
from zipfile import ZipFile
import telebot, time


API_TOKEN = 'YOUR_TOKEN'
bot: TeleBot = telebot.TeleBot(API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


def markup_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    smm_spec = types.KeyboardButton("SMM-специалист" + "(" + str(len(smm)) + ")")
    targetolog = types.KeyboardButton("Таргетолог" + "(" + str(len(tgt)) + ")")
    designer = types.KeyboardButton("Дизайнер" + "(" + str(len(des)) + ")")
    bloger_manager = types.KeyboardButton("Менеджер блогеров" + "(" + str(len(blgmngr)) + ")")
    copyrighter = types.KeyboardButton("Копирайтер" + "(" + str(len(copy)) + ")")
    tech_spec = types.KeyboardButton("Технический специалист" + "(" + str(len(teh)) + ")")
    about_button = types.KeyboardButton("О проекте")
    markup.add(smm_spec, targetolog)
    markup.add(designer, bloger_manager)
    markup.add(copyrighter, tech_spec)
    markup.add(about_button)
    return markup

def make_arch():
    with ZipFile("analitics.zip", "w") as newzip:
        newzip.write("about.csv")
        newzip.write("blog_manager.csv")
        newzip.write("copyrighter.csv")
        newzip.write("designer.csv")
        newzip.write("smm.csv")
        newzip.write("start.csv")
        newzip.write("targetolog.csv")
        newzip.write("techno_spec.csv")

def send_zip(message):
    bot.send_document(message.chat.id, open("analitics.zip", 'rb'))

def write_to_file(message, fname):
    tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))
    file = open(fname+'.csv', 'a')
    line = '{id},{username},{first},{last},{date}\n'.format(id=message.chat.id, username=message.from_user.username,
                                                     first=message.from_user.first_name,
                                                     last=message.from_user.last_name,
                                                     date=tconv(message.date))
    file.write(line)
    file.close()

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    write_to_file(message, "start")
    bot.send_message(message.chat.id, message.from_user.first_name + ", привет! Кого вы ищете?",
                     reply_markup=markup_keyboard())

@bot.message_handler(commands=['zip'])
def send_analitics(message):
    adm = [ADMIN_ID]
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'ACCESS DENIED')
    else:
        make_arch()
        send_zip(message)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    if 'SMM-специалист' in message.text:
        write_to_file(message, "smm")
        send_character_page(message)
    elif 'Таргетолог' in message.text:
        write_to_file(message, "targetolog")
        send_targetolog(message)
    elif 'Дизайнер' in message.text:
        write_to_file(message, "designer")
        send_designer(message)
    elif 'Менеджер блогеров' in message.text:
        write_to_file(message, "blog_manager")
        send_bloger(message)
    elif 'Копирайтер' in message.text:
        write_to_file(message, "copyrighter")
        send_copyrighter(message)
    elif 'Технический специалист' in message.text:
        write_to_file(message, "techno_spec")
        send_teh_spec(message)
    elif 'О проекте' in message.text:
        write_to_file(message, "about")
        bot.send_message(message.chat.id, about, parse_mode='Markdown', disable_web_page_preview=True)


# SMM

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'smm')
def smm_callback(call):
        page = int(call.data.split('#')[1])
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        send_character_page(call.message, page)


def send_character_page(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(smm),
        current_page=page,
        data_pattern='smm#{page}'
    )

    paginator.add_after(InlineKeyboardButton('О проекте', callback_data='about'))

    bot.send_message(
        message.chat.id,
        smm[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


# Target

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'target')
def target_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_targetolog(call.message, page)


def send_targetolog(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(tgt),
        current_page=page,
        data_pattern='target#{page}'
    )

    paginator.add_after(InlineKeyboardButton('О проекте', callback_data='about'))

    bot.send_message(
        message.chat.id,
        tgt[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


# Design

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'design')
def target_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_designer(call.message, page)


def send_designer(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(des),
        current_page=page,
        data_pattern='design#{page}'
    )

    paginator.add_after(InlineKeyboardButton('О проекте', callback_data='about'))

    bot.send_message(
        message.chat.id,
        des[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


# Bloger-manager

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'bloger')
def target_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_bloger(call.message, page)


def send_bloger(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(blgmngr),
        current_page=page,
        data_pattern='bloger#{page}'
    )

    paginator.add_after(InlineKeyboardButton('О проекте', callback_data='about'))

    bot.send_message(
        message.chat.id,
        blgmngr[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


# Copyrighter


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'copy')
def target_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_copyrighter(call.message, page)


def send_copyrighter(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(copy),
        current_page=page,
        data_pattern='copy#{page}'
    )

    paginator.add_after(InlineKeyboardButton('О проекте', callback_data='about'))

    bot.send_message(
        message.chat.id,
        copy[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


# Tech Specialist


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'tech_spec')
def target_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )

    send_teh_spec(call.message, page)


def send_teh_spec(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(teh),
        current_page=page,
        data_pattern='tech_spec#{page}'
    )

    paginator.add_after(InlineKeyboardButton('О проекте', callback_data='about'))

    bot.send_message(
        message.chat.id,
        teh[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


# ABOUT


@bot.callback_query_handler(func=lambda call: call.data == 'about')
def about_callack(call):
    bot.send_message(call.message.chat.id, about, parse_mode='Markdown', disable_web_page_preview=True)


bot.infinity_polling()
