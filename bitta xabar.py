import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# Tokenni olish
TOKEN = os.getenv("BOT_TOKEN")

# Xabar yuboriladigan foydalanuvchi ID sini bu yerda kiriting
USER_ID = "1360061767"  # <-- Bu yerga o'z foydalanuvchi ID'ingizni yozing

async def send_message_to_user():
    bot = Bot(token=TOKEN)
    
    try:
        await bot.send_message(
            chat_id=USER_ID,
            text="🤖 *Bot qayta ishga tushdi!* \n"
                 "Agar muammo bo'lsa, /start ni bosib qayta ishlating!\nHurmatli foydalanuvchi faol obunachi maqomi oldingiz hamda botdan foydalanish uchun 50 ta limit qolga kiritdingiz!",
            parse_mode="Markdown"
        )
        print(f"✅ Xabar yuborildi: {USER_ID}")
    except Exception as e:
        print(f"❌ Xatolik ({USER_ID}): {e}")

if __name__ == "__main__":
    asyncio.run(send_message_to_user())
