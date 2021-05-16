import telebot
import speech_recognition as sr
import subprocess

r = sr.Recognizer()
Token = '1873974788:AAG-1wbZTOwhYAuwe840qTnx8ZnRFkO4heM'
bot = telebot.TeleBot(Token)

# Глобальные переменные для смены языка
EN = 'en-GB'
RU = 'ru-RU'
LAN = RU # По умолчанию используется русский язык 


# Приветственное сообщение
@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, "Привет! Отправь голосовое сообщение")


# Команда /language вызывает две кнопки, которые записывают в callback текущий язык
@bot.message_handler(commands=['language'])
def language_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='English', callback_data=EN))
    markup.add(telebot.types.InlineKeyboardButton(text='Русский', callback_data=RU))
    bot.send_message(message.chat.id, text="Пожалуйста, выберите язык распознования речи", reply_markup=markup)


# Обработка смены языка, изменяется глобальная переменная LAN, которая используется в функции recognize_google, а также печатается сообщение о смене языка
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = ''
    global LAN
    if call.data == EN:
        answer = 'Now bot use English (United Kingdom). Thank you!'
        LAN = EN
    elif call.data == RU:
        answer = 'Теперь бот использует русский язык. Спасибо!'
        LAN = RU
    bot.send_message(call.message.chat.id, answer)


@bot.message_handler(content_types=['voice'])
def handle(message):
    # запись голосового сообщения от пользователя в audio.ogg
    fileID = message.voice.file_id
    file = bot.get_file(fileID)
    down_file = bot.download_file(file.file_path)
    with open('audio.ogg', 'wb') as f:
        f.write(down_file)

    # конвертация audio.ogg в audio.wav с помощью приложения ffmpeg
    process = subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])

    # использование библиотеки speech_recognition для преобращования audio.wav в текстовое сообщение
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


# условие, для того, чтобы бот постоянно ожидал запрос от пользователя в конце
if __name__ == '__main__':
    bot.infinity_polling()
