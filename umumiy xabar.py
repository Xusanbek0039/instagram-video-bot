import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# Tokenni olish
TOKEN = os.getenv("BOT_TOKEN")
USER_FILE = "user_limits.txt"

async def send_startup_message():
    bot = Bot(token=TOKEN)
    
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split(" ")
            if len(parts) < 1:
                continue  # Bo'sh yoki noto'g'ri formatdagi qatordan o'tib ketamiz
            
            user_id = parts[0]  # Birinchi ustun - foydalanuvchi ID
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text="🤖 *Robot faol ishlamoqda foydalanish uchun iltimos Instagram Reels video havolasini yuboring!* \n",
                    parse_mode="Markdown"
                )
                print(f"✅Xabar yuborildi: {user_id}")
            except Exception as e:
                print(f"❌Xatolik ({user_id}): {e}")

    except FileNotFoundError:
        print("❌ user_limits.txt fayli topilmadi!")

if __name__ == "__main__":
    asyncio.run(send_startup_message())