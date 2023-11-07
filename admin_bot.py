# t.me/x1larusAdmin_bot
# 6707786949:AAHrncqIuJkKOj2POlphL-xubIkog4Nmy9o

import telebot
import os
import uuid
import qrcode


# GLOVAL VARIABLES ========================================
bot = telebot.TeleBot('6707786949:AAHrncqIuJkKOj2POlphL-xubIkog4Nmy9o')
g_userbotname = 'x1larusUser_bot'
g_contents_path = os.getcwd() + '\\contents'
g_active_users = dict()
g_phrases = {
    'not_active': 'Вы не вошли в режим записи контента. Введите /new_content',
    'welcome' : 'салам алейкум, лучший crm эвер',
    'new_content': 'Вы вошли в режим записи контента. Скидывайте по одному файлы или текстовые сообщения. Когда закончите, напишите /end_content',
    'qr_notif': 'Данные загружены. Вы можете получить их по данному qr-коду:'
}

# GLOBAL VARIABLES END


# HANDLERS ==================================================
@bot.message_handler(commands=['start'])
def start(message : telebot.types.Message):
    bot.send_message(message.chat.id, g_phrases['welcome'])


@bot.message_handler(commands=['new_content'])
def new_content(message : telebot.types.Message):
    bot.send_message(message.chat.id, g_phrases['new_content'])
    uid = str(uuid.uuid1())
    os.mkdir(g_contents_path + f'\\{uid}')
    g_active_users[message.from_user.id] = uid


@bot.message_handler(content_types=['document', 'video', 'audio'])
def handle_file(message):
    if not(message.from_user.id in g_active_users):
        bot.send_message(message.chat.id, g_phrases['not_active'])
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = g_contents_path + f'\\{g_active_users[message.from_user.id]}\\' + message.document.file_name  # сохраняем файл с его исходным именем
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, 'Файл сохранен!')


@bot.message_handler(commands=['end_content'])
def end_content(message : telebot.types.Message):
    if not(message.from_user.id in g_active_users):
        bot.send_message(message.chat.id, g_phrases['not_active'])
        return
    bot.send_message(message.chat.id, g_phrases['qr_notif'])
    bot.send_photo(message.chat.id, open(generate_and_save_qr(g_active_users[message.from_user.id]), 'rb'))
    g_active_users.pop(message.from_user.id)



# HANDLERS END
    
# SERVICE FINCTIONS =================================================

# returns savepath
def generate_and_save_qr(uid : str) -> str:
    qr = qrcode.make(f'https://t.me/{g_userbotname}?start={uid}')
    path = f'{g_contents_path}\\{uid}\\qr.png'
    qr.save(path)
    return path


bot.polling()