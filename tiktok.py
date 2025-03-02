import os
import yt_dlp
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot tokeningizni shu yerga kiriting
BOT_TOKEN = "6849473588:AAEnKvipTVegay2YVhTaFPT2PBImHiNG0xA"

def expand_tiktok_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, allow_redirects=True, timeout=30, headers=headers, verify=False)
        return response.url if response.status_code == 200 else url
    except requests.exceptions.RequestException as e:
        print(f"❌ URLni ochishda xatolik: {e}")
        return None

def download_tiktok_video(url):
    try:
        expanded_url = expand_tiktok_url(url)
        if not expanded_url:
            return None
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'tiktok_video.mp4',
            'socket_timeout': 60,
            'noprogress': False,
            'quiet': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([expanded_url])
        
        if os.path.exists("tiktok_video.mp4"):
            with open("tiktok_video.mp4", "rb") as video_file:
                return video_file.read()
        return None
    except Exception as e:
        print(f"❌ TikTok yuklashda xatolik: {e}")
        return None

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    
    if "tiktok.com" in text or "vt.tiktok.com" in text:
        await update.message.reply_text("⏳ TikTok videosi yuklanmoqda... Iltimos, kuting.")
        video_content = download_tiktok_video(text)
        
        if video_content:
            await update.message.reply_video(video=video_content, caption="Sizning TikTok videosi 🎥")
            if os.path.exists("tiktok_video.mp4"):
                os.remove("tiktok_video.mp4")
        else:
            await update.message.reply_text("❌ Video yuklab olinmadi. Havolani tekshirib, qaytadan yuboring!")
    else:
        await update.message.reply_text("❌ Iltimos, faqat TikTok video havolasini yuboring!")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Assalomu alaykum! TikTok video yuklab beruvchi botga xush kelibsiz. Havolani yuboring!")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot ishga tushdi!")
    app.run_polling()