import telebot
import os
import requests
import pytesseract
import speech_recognition as sr
from PIL import Image

bot = telebot.TeleBot('your token')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello, welcome to my bot!\n press /tutorial for usage ')

@bot.message_handler(commands=['tutorial'])
def send_welcome(message):
    bot.reply_to(message, 'Hey,if you send a photo i give you a text\nif you send a text i give you answer\nif you send a voice message i convert it to text')

@bot.message_handler(content_types=['photo'])
def image_to_text(message):
    file_id = message.photo[-1].file_id
    file_url = f'https://api.telegram.org/bot{bot.token}/getfile?file_id={file_id}'
    file_path = requests.get(file_url).json()['result']['file_path']
    image_url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'
    response = requests.get(image_url, verify=False)
    with open('image.jpg', 'wb') as f:
        f.write(response.content)
    text = pytesseract.image_to_string(Image.open('image.jpg'))
    bot.reply_to(message, text)


bot.polling()
