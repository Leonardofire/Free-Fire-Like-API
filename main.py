import telebot
import requests

TOKEN = "8938915066:AAFQZGTZla9H2E4L3wMo8QwpDFUhyLOnWa0"

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 **Привет!**\n\n"
        "Отправь мне **UID игрока Free Fire**, и я загружу информацию о его профиле!"
    )

@bot.message_handler(func=lambda message: message.text and message.text.isdigit())
def process_uid(message):
    uid = message.text.strip()
    status_msg = bot.reply_to(message, "🔄 *Запрашиваю данные с сервера Free Fire...*")
    
    url = f"https://freefireinfo-zy9l.onrender.com/api/v1/player-profile?uid={uid}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            basic = data.get("basicInfo", {})
            
            nickname = basic.get("nickname", "Неизвестно")
            level = basic.get("level", "Н/Д")
            likes = basic.get("liked", 0)
            region = basic.get("region", "Н/Д")
            
            text = (
                f"🎮 **Профиль игрока Free Fire**\n\n"
                f"👤 **Никнейм:** `{nickname}`\n"
                f"🆔 **UID:** `{uid}`\n"
                f"⭐ **Уровень:** `{level}`\n"
                f"👍 **Лайки:** `{likes}`\n"
                f"🌍 **Регион:** `{region}`"
            )
            bot.edit_message_text(
                text, 
                chat_id=status_msg.chat.id, 
                message_id=status_msg.message_id,
                parse_mode="Markdown"
            )
        else:
            bot.edit_message_text(
                "❌ **Игрок с таким UID не найден или сервер API недоступен.**", 
                chat_id=status_msg.chat.id, 
                message_id=status_msg.message_id
            )
    except Exception:
        bot.edit_message_text(
            "⚠️ **Не удалось подключиться к серверу игры.** Попробуйте позже.", 
            chat_id=status_msg.chat.id, 
            message_id=status_msg.message_id
        )

if __name__ == '__main__':
    bot.infinity_polling()
    
