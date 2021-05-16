import telebot
import speech_recognition as sr
import subprocess

r = sr.Recognizer()
token = '1873974788:AAG-1wbZTOwhYAuwe840qTnx8ZnRFkO4heM'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def command_start(message):
    # приветственное сообщение
    bot.send_message(message.chat.id, "Привет! Отправь голосовое сообщение")


@bot.message_handler(content_types=['voice'])
def handle(message):
    #запись голосового сообщения от пользователя в audio.ogg
    fileID = message.voice.file_id
    file = bot.get_file(fileID)
    down_file = bot.download_file(file.file_path)
    with open('audio.ogg', 'wb') as f:
        f.write(down_file)

    #конвертация audio.ogg в audio.wav с помощью приложения ffmpeg
    process = subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])

    #использование библиотеки speech_recognition для преобращования audio.wav в текстовое сообщение
    file = sr.AudioFile('audio.wav')
    with file as source:
        try:
            audio = r.record(source)
            text = r.recognize_google(audio, language='ru-RU`')
            bot.send_message(message.chat.id, text)
        except sr.UnknownValueError:
            bot.send_message(message.chat.id, "Произошла ошибка при распознавании голоса!")

bot.polling(none_stop=True)
