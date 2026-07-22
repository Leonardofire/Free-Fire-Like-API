import telebot
import requests

TOKEN = "8938915066:AAF0ZGTIaOH2E4LM3wfb8qupDFUyLOniwa0"

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 **Привет!**\n\n"
        "Отправь мне **UID игрока Free Fire**, чтобы получить информацию о профиле."
    )

@bot.message_handler(func=lambda message: message.text and message.text.isdigit())
def process_uid(message):
    uid = message.text.strip()
    status_msg = bot.reply_to(message, "🔄 *Запрашиваю данные с серверов Free Fire...*")
    
    # Запрос к профильному API
    url = f"https://freefireinfo-zy9l.onrender.com/api/v1/player-profile?uid={uid}"
    
    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Проверка ответа на наличие информации
            if not isinstance(data, dict) or ("basicInfo" not in data and "basic_info" not in data):
                bot.edit_message_text(
                    "❌ **Игрок с таким UID не найден.** Проверьте правильность введенных цифр.", 
                    chat_id=status_msg.chat.id, 
                    message_id=status_msg.message_id
                )
                return

            basic = data.get("basicInfo") or data.get("basic_info", {})
            clan = data.get("clanBasicInfo") or data.get("clan_info", {})
            social = data.get("socialInfo") or data.get("social_info", {})
            
            nickname = basic.get("nickname") or basic.get("name", "Неизвестно")
            level = basic.get("level", "Н/Д")
            likes = basic.get("liked") or basic.get("likes", 0)
            region = basic.get("region", "Н/Д")
            bio = social.get("signature", "Отсутствует")
            guild_name = clan.get("clanName") or clan.get("name", "Нет гильдии")
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
                f"⚠️ **Ошибка API (код {response.status_code}).** Внешний сервер с данными временно недоступен. Попробуйте через пару минут.", 
                chat_id=status_msg.chat.id, 
                message_id=status_msg.message_id
            )
            
    except requests.exceptions.Timeout:
        bot.edit_message_text(
            "⏳ **Сервер API слишком долго отвечает.** (На Render бесплатные API «засыпают» при простое и просыпаются за 30-40 секунд). Попробуйте отправить UID ещё раз!", 
            chat_id=status_msg.chat.id, 
            message_id=status_msg.message_id
        )
    except Exception as e:
        bot.edit_message_text(
            "⚠️ **Не удалось обработать запрос.** Попробуйте чуть позже.", 
            chat_id=status_msg.chat.id, 
            message_id=status_msg.message_id
        )

if __name__ == '__main__':
    bot.infinity_polling()
    
