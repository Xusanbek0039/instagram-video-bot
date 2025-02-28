import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import os
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# Tokenni olish
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchilar ro'yxatini olish uchun funksiya
def get_users_from_file():
    users = []
    with open("user_limits.txt", "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if parts:
                user_id = parts[0]  # Foydalanuvchi IDsi birinchi qator
                if user_id.isdigit():
                    users.append(int(user_id))
    return users

# /sendall komandasi
@dp.message(Command("sendall"))
async def send_all(message: Message):
    users = get_users_from_file()
    sent_count = 0
    failed_count = 0

    for user_id in users:
        try:
            await bot.send_message(user_id, "Salom! Bu umumiy xabar! 🔥\nBotimizda kunlik foydalanish mumkin bo'lgan limit 20 taga ko'paydi!!! /start bosing va limitingizdan foydalaning!")
            sent_count += 1
            await asyncio.sleep(0.5)  # Antispam uchun
        except:
            failed_count += 1

    await message.answer(f"✅ {sent_count} ta foydalanuvchiga xabar yuborildi!\n❌ {failed_count} ta foydalanuvchiga yuborilmadi.")

# Botni ishga tushirish
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Bot ishlamoqda!")
    asyncio.run(main())
