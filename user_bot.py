# t.me/x1larusUser_bot
# 6930288520:AAF_cCWJbNvG5BZ2oh1tcn_xktS35rPehbU

import telebot
import os


# GLOBAL VARIABLES ==============================
g_contents_path = os.getcwd() + '\\contents'
bot = telebot.TeleBot('6930288520:AAF_cCWJbNvG5BZ2oh1tcn_xktS35rPehbU')
g_phrases = {
    'invalid_params': 'Неверные входные параметры',
}



# HANDLERS ======================================
@bot.message_handler(commands=['start'])
def start(message : telebot.types.Message):
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, g_phrases['invalid_params'])
        return
    uid = args[1].strip()
    
    path = f'{g_contents_path}\\{uid}'
    list_files = os.listdir(path)
    list_files.remove('qr.png')
    list_files.remove('text')
    
    for file in list_files:
        with open (f'{path}\\{file}', 'rb') as f:
            bot.send_document(message.chat.id, f)
    
    list_texts = os.listdir(path + '\\text')
    for file in list_texts:
        with open(f'{path}\\text\\{file}', 'r', encoding='UTF-8') as f:
            bot.send_message(message.chat.id, f.read())


bot.polling()