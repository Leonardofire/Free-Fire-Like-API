import telebot
import requests

TOKEN = "8938915066:AAF0ZGTIaOH2E4LM3wfb8qupDFUyLOniwa0"

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 **Привет!**\n\n"
        "Отправь мне **UID игрока Free Fire**, и я загружу реальную информацию о профиле!"
    )

@bot.message_handler(func=lambda message: message.text and message.text.isdigit())
def process_uid(message):
    uid = message.text.strip()
    status_msg = bot.reply_to(message, "🔄 *Запрашиваю данные с серверов Free Fire...*")
    
    # Используем стабильный публичный API для получения данных игрока
    url = f"https://ff-api-info.vercel.app/api/player?uid={uid}"
    
    try:
        response = requests.get(url, timeout=12)
        if response.status_code == 200:
            data = response.json()
            
            # Проверяем, вернул ли API ошибку или пустые данные
            if "error" in data or not data.get("basicInfo"):
                bot.edit_message_text(
                    "❌ **Игрок с таким UID не найден.** Проверьте правильность введенных цифр.", 
                    chat_id=status_msg.chat.id, 
                    message_id=status_msg.message_id
                )
                return

            basic = data.get("basicInfo", {})
            clan = data.get("clanBasicInfo", {})
            social = data.get("socialInfo", {})
            
            nickname = basic.get("nickname", "Неизвестно")
            level = basic.get("level", "Н/Д")
            likes = basic.get("liked", 0)
            region = basic.get("region", "Н/Д")
            bio = social.get("signature", "Отсутствует")
            guild_name = clan.get("clanName", "Нет гильдии")
            guild_level = clan.get("clanLevel", "-")
            
            text = (
                f"🎮 **Профиль игрока Free Fire**\n\n"
                f"👤 **Никнейм:** `{nickname}`\n"
                f"🆔 **UID:** `{uid}`\n"
                f"⭐ **Уровень:** `{level}`\n"
                f"👍 **Лайки:** `{likes}`\n"
                f"🌍 **Регион:** `{region}`\n"
                f"🛡️ **Гильдия:** `{guild_name}` (Ур. {guild_level})\n"
                f"📝 **Подпись:** _{bio}_"
            )
            
            bot.edit_message_text(
                text, 
                chat_id=status_msg.chat.id, 
                message_id=status_msg.message_id,
                parse_mode="Markdown"
            )
        else:
            bot.edit_message_text(
                f"❌ **Ошибка API (код {response.status_code}):** Сервер Free Fire временно недоступен.", 
                chat_id=status_msg.chat.id, 
                message_id=status_msg.message_id
            )
    except Exception:
        bot.edit_message_text(
            "⚠️ **Превышено время ожидания ответа.** Попробуйте отправить UID ещё раз через пару секунд.", 
            chat_id=status_msg.chat.id, 
            message_id=status_msg.message_id
        )

if __name__ == '__main__':
    bot.infinity_polling()
    
