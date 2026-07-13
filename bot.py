import telebot
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "আসালামু আলাইকুম সোনা! আমি অন আছি ✅")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"তুমি বললা: {message.text}")

print("Bot is running...")
bot.polling(none_stop=True)
