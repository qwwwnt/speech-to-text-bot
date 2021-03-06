import telebot
import speech_recognition as sr
import subprocess
import languages as l

r = sr.Recognizer()
from config import Token

bot = telebot.TeleBot(Token)


# Приветственное сообщение
@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, "Привет! ✋ Отправь голосовое сообщение")


# Команда /language вызывает две кнопки, которые записывают в callback текущий язык
@bot.message_handler(commands=['language'])
def language_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='English 🇬🇧', callback_data=l.EN))
    markup.add(telebot.types.InlineKeyboardButton(text='Русский 🇷🇺', callback_data=l.RU))
    markup.add(telebot.types.InlineKeyboardButton(text='Français 🇫🇷', callback_data=l.FR))
    markup.add(telebot.types.InlineKeyboardButton(text='Deutsche 🇩🇪', callback_data=l.DE))
    markup.add(telebot.types.InlineKeyboardButton(text='日本語 🇯🇵', callback_data=l.JP))
    bot.send_message(message.chat.id, text="Пожалуйста, выберите язык распознавания речи", reply_markup=markup)


# Обработка смены языка, изменяется глобальная переменная LAN, которая используется в функции recognize_google, а также печатается сообщение о смене языка
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = ''
    global LAN
    if call.data == l.EN:
        answer = 'Now bot use English (United Kingdom). Thank you!'
        LAN = l.EN
    elif call.data == l.RU:
        answer = 'Теперь бот использует русский язык. Спасибо!'
        LAN = l.RU
    elif call.data == l.FR:
        answer = 'Le bot utilise désormais le français. Merci!'
        LAN = l.FR
    elif call.data == l.DE:
        answer = 'Der Bot spricht jetzt Deutsch. Danke!'
        LAN = l.DE
    elif call.data == l.JP:
        answer = 'ボットは現在、日本語を使用しています。 ありがとうございました！'
        LAN = l.JP
    bot.send_message(call.message.chat.id, answer)


@bot.message_handler(content_types=['voice'])
def handle(message):
    # Запись голосового сообщения от пользователя в audio.ogg
    fileID = message.voice.file_id
    file = bot.get_file(fileID)
    down_file = bot.download_file(file.file_path)
    with open('audio.ogg', 'wb') as f:
        f.write(down_file)

    # Конвертация audio.ogg в audio.wav с помощью приложения ffmpeg
    process = subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])

    # Использование библиотеки speech_recognition для преобращования audio.wav в текстовое сообщение
    file = sr.AudioFile('audio.wav')
    with file as source:
        try:
            audio = r.record(source)
            global LAN
            text = r.recognize_google(audio, language=LAN)
            bot.send_message(message.chat.id, text)
        # Обработка неудачного распознавания сообщения
        except sr.UnknownValueError:
            bot.send_message(message.chat.id, "Произошла ошибка при распознавании голоса!")


# Сообщение, которое выводится при запуске /help
answer_help = '''
    Привет! ✋ Этот бот переводит в текст голосовые сообщения, которые получает. 
    
Команды, которые использует бот:
    /help — Это сообщение)
    /start — Начало диалога
    /language — Выбор языка распознавания речи. Доступны Русский, Английский, Французский, Немецкий, Японский
    
Вопросы и пожелания отправляйте сюда — @speech_bot_questions_bot
'''


# Функция для команды /help
@bot.message_handler(commands=['help'])
def process_help_command(message):
    bot.send_message(message.chat.id, answer_help)


# Условие, для того, чтобы бот постоянно ожидал запрос от пользователя в конце
if __name__ == '__main__':
    bot.infinity_polling()
