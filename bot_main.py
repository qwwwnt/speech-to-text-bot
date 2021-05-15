import telebot
import speech_recognition as sr
import subprocess

r = sr.Recognizer()
token = '1873974788:AAG-1wbZTOwhYAuwe840qTnx8ZnRFkO4heM'
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['voice'])
def handle(message):
    fileID = message.voice.file_id
    file = bot.get_file(fileID)
    down_file = bot.download_file(file.file_path)
    with open('audio.ogg', 'wb') as f:
        f.write(down_file)

    process = subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y']) #конвертация audio.ogg в audio.wav

    file = sr.AudioFile('audio.wav')
    with file as source:
        audio = r.record(source)
        text = r.recognize_google(audio, language='ru-RU`')
        bot.send_message(message.chat.id, text)
    
bot.polling(none_stop=True)
