import telebot
from telebot import types

from ColorTransfer import ColorTranseferer
from ConfigTelebot import TOKEN

bot = telebot.TeleBot(TOKEN)

global_buttons = types.ReplyKeyboardMarkup()
glob_btn = types.KeyboardButton('START')
global_buttons.add(glob_btn)

# in use may be needed to make the database
dict_chat_id_photos_to = {}
dict_chat_id_photos_from = {}
dict_chat_id_metrics = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    buttons = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("Quadratic", callback_data='C_2')
    btn2 = types.InlineKeyboardButton("Linear", callback_data='C_1')
    buttons.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     "Hello! I'm a Color-Transfer Bot and I'm here to transfer color from one of your photo to another",
                     reply_markup=global_buttons)
    bot.send_message(message.chat.id, "Choose the metric, which I use to transfer the color:", reply_markup=buttons)


@bot.callback_query_handler(func=lambda call: True)
def get_metric(call):
    if call.message.text == 'START':
        send_welcome(call.message)
    if call.data == 'C_2':
        dict_chat_id_metrics[call.message.chat.id] = 'C_2'
    elif call.data == 'C_1':
        dict_chat_id_metrics[call.message.chat.id] = 'C_1'
    bot.send_message(call.message.chat.id,
                     "Send me the photo TO which I will transfer the color")
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, get_first_photo)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'START':
        send_welcome(message)
        return
    bot.reply_to(message, message.text)


def get_first_photo(message):
    if message.content_type == 'document':
        dict_chat_id_photos_to[message.chat.id] = bot.download_file(bot.get_file(message.document.file_id).file_path)
    elif message.content_type == 'photo':
        dict_chat_id_photos_to[message.chat.id] = bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)
    elif message.text == '/start' or message.text == '/help' or message.text == 'START':
        send_welcome(message)
        return
    else:
        bot.send_message(message.chat.id, "Please, send me the photo TO which I will transfer the color!")
        bot.register_next_step_handler_by_chat_id(message.chat.id, get_first_photo)
        return
    bot.send_message(message.chat.id, "Nice! Then, send me the photo FROM which I will transfer the color")
    bot.register_next_step_handler_by_chat_id(message.chat.id, get_second_photo)


def get_second_photo(message):
    if message.content_type == 'document':
        dict_chat_id_photos_from[message.chat.id] = bot.download_file(bot.get_file(message.document.file_id).file_path)
    elif message.content_type == 'photo':
        dict_chat_id_photos_from[message.chat.id] = bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)
    elif message.text == '/start' or message.text == '/help' or message.text == 'START':
        send_welcome(message)
        return
    else:
        bot.send_message(message.chat.id, "Please, send me the photo FROM which I will transfer the color!")
        bot.register_next_step_handler_by_chat_id(message.chat.id, get_first_photo)
        return
    # bot.register_next_step_handler_by_chat_id(message.chat.id, process_transfer)
    process_transfer(message)


def process_transfer(message):
    bot.send_message(message.chat.id, "Good! Now I will process your photo and give you the result")
    transferer = ColorTranseferer(dict_chat_id_photos_to[message.chat.id], dict_chat_id_photos_from[message.chat.id])
    img_str = transferer.transfer_color(method=dict_chat_id_metrics[message.chat.id])
    bot.send_message(message.chat.id, "That's your photo with transfered color!")
    bot.send_photo(message.chat.id, img_str)
    send_welcome(message)


bot.infinity_polling()
