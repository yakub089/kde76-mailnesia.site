import telebot
from telebot import types
import os

TOKEN = "8989526607:AAEcVrrIo04v9SmQEfCLzj1qC658gVS57BM"
bot = telebot.TeleBot(TOKEN)

# তোমার দেওয়া Channel ID
CHANNEL1 = -1002637580522 # OTP Group
CHANNEL2 = -1003992566258 # Support Group
ADMIN_ID = 7416697908  # <-- এই লাইনটা নতুন যোগ করো এখানে

# User data temp save করার জন্য
user_data = {}
balance = {}

# Force Join Check
def check_join(user_id):
    try:
        ch1 = bot.get_chat_member(CHANNEL1, user_id).status
        ch2 = bot.get_chat_member(CHANNEL2, user_id).status
        return ch1 in ['member', 'administrator', 'creator'] and ch2 in ['member', 'administrator', 'creator']
    except:
        return False

# Main Keyboard
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📱 Get Number", "🔑 2Fa")
    markup.row("🤖 Api Number", "🚦 Live Traffic")
    markup.row("🌐 Language")
    markup.row("💸 Withdraw", "💰 Balance")
    return markup
    @bot.message_handler(func=lambda message: message.text == 'facebook')
def facebook_countries(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🇧🇩 Bangladesh'),
        types.KeyboardButton('🇮🇳 India'),
        types.KeyboardButton('🇺🇸 USA'),
        types.KeyboardButton('🇬🇧 UK'),
        types.KeyboardButton('🔙 Back')
    )
    bot.send_message(message.chat.id, "দেশ সিলেক্ট করো:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'instagram')
def instagram_countries(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🇧🇩 Bangladesh'),
        types.KeyboardButton('🇮🇳 India'),
        types.KeyboardButton('🇺🇸 USA'),
        types.KeyboardButton('🇬🇧 UK'),
        types.KeyboardButton('🔙 Back')
    )
    bot.send_message(message.chat.id, "দেশ সিলেক্ট করো:", reply_markup=markup)

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not check_join(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 OTP Group", url="https://t.me/c/2637580522"))
        markup.add(types.InlineKeyboardButton("📢 Support Group", url="https://t.me/c/3992566258"))
        markup.add(types.InlineKeyboardButton("✅ Verify Now", callback_data="verify"))
        bot.send_message(message.chat.id, "বট ব্যবহার করতে ২ টা চ্যানেলে জয়েন করো সোনা", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "আসালামু আলাইকুম সোনা! আমি অন আছি ✅", reply_markup=main_keyboard())

# Verify Button
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if check_join(call.from_user.id):
        bot.send_message(call.message.chat.id, "ভেরিফাই সফল ✅", reply_markup=main_keyboard())
    else:
        bot.answer_callback_query(call.id, "আগে ২ টা চ্যানেলে জয়েন করো")

# Get Number
@bot.message_handler(func=lambda m: m.text == "📱 Get Number")
def get_number_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("facebook", callback_data="fb"))
    markup.add(types.InlineKeyboardButton("instagram", callback_data="ig"))
    bot.send_message(message.chat.id, "Platform সিলেক্ট করো", reply_markup=markup)

# API Keyboard
def api_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔢 Set Range", "📱 Get API Number", "⬅️ Back")
    return markup

# API Number
@bot.message_handler(func=lambda m: m.text == "🤖 Api Number")
def api_number_menu(message):
    bot.send_message(message.chat.id, "API Panel", reply_markup=api_keyboard())

@bot.message_handler(func=lambda m: m.text == "🔢 Set Range")
def set_range(message):
    msg = bot.send_message(message.chat.id, "Please enter the Range ID (e.g., 22898):")
    bot.register_next_step_handler(msg, save_range)

def save_range(message):
    user_data[message.from_user.id] = {"range": message.text}
    bot.send_message(message.chat.id, f"✅ Range saved: {message.text}", reply_markup=api_keyboard())

@bot.message_handler(func=lambda m: m.text == "📱 Get API Number")
def get_api(message):
    uid = message.from_user.id
    if uid not in user_data or "range" not in user_data[uid]:
        bot.send_message(message.chat.id, "আগে Range সেট করো")
        return
    bot.send_message(message.chat.id, """✅ Number Allocated
📱 Number: +224657176849
🌍 Country: Guinea
📡 Operator: Mobile
🔢 Range: 22465XXX
⏳ Waiting for OTP...""")

@bot.message_handler(func=lambda m: m.text == "⬅️ Back")
def back(message):
    bot.send_message(message.chat.id, "Main Menu", reply_markup=main_keyboard())
# Balance
@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance_check(message):
    uid = message.from_user.id
    bal = balance.get(uid, 0)
    bot.send_message(message.chat.id, f"💰 Your Balance: {bal} ৳\nপ্রতি OTP = 0.10 ৳")

bot.polling(none_stop=True)
