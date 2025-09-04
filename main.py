import asyncio
import os
import re
import tempfile
from contextlib import suppress
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- Yordamchi: URL tekshirish
INSTAGRAM_URL_RE = re.compile(
    r"(https?://)?(www\.)?(instagram\.com|instagr\.am)/[^\s]+",
    re.IGNORECASE,
)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
COOKIES_FILE = os.getenv("COOKIES_FILE")  # ixtiyoriy
MAX_MB = int(os.getenv("MAX_MB", "45"))   # Telegram’da xavfsiz limit sifatida 45MB

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN .env faylida ko'rsatilmagan")

HELP_TEXT = (
    "Assalomu alaykum! Menga Instagram post/reels havolasini yuboring — videoni yuklab beraman.\n\n"
    "Qo'llab-quvvatlanadi: Reels va Post (public). Agar video private bo'lsa, cookies bilan yana urinib ko'ring.\n"
    f"Yuklash hajm limiti: ~{MAX_MB}MB.\n\n"
    "Buyruqlar:\n"
    "/start — Botni ishga tushirish\n"
    "/help — Yordam"
)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! 👋 Instagram havolasini yuboring, men videoni olib beraman.\n\n" + HELP_TEXT)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)

def _human_size(num_bytes: int) -> str:
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024
    if num_bytes >= gb: return f"{num_bytes/gb:.2f} GB"
    if num_bytes >= mb: return f"{num_bytes/mb:.2f} MB"
    if num_bytes >= kb: return f"{num_bytes/kb:.2f} KB"
    return f"{num_bytes} B"

async def _run_yt_dlp(url: str, target_dir: Path, cookies_file: str | None):
    """
    yt-dlp ni asyncio bloklamasdan ishga tushirish.
    Eng yaxshi MP4 formatni yuklab oladi va local fayl yo'lini qaytaradi.
    """
    from yt_dlp import YoutubeDL

    ydl_opts = {
        # Eng yaxshi *video+audio* MP4 varianti:
        "format": "bv*[ext=mp4]+ba*[ext=m4a]/b[ext=mp4]/bv*+ba/b",
        "outtmpl": str(target_dir / "%(title).200B.%(id)s.%(ext)s"),
        "noprogress": True,
        "quiet": True,
        "merge_output_format": "mp4",
    }
    if cookies_file and Path(cookies_file).exists():
        ydl_opts["cookiefile"] = cookies_file

    def _download():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Agar playlist/karusel bo'lsa, birinchi elementni olamiz
            if "entries" in info and info["entries"]:
                info = info["entries"][0]
            filename = ydl.prepare_filename(info)
            # Post-process natijaviy kengaytma .mp4 bo'lishi mumkin
            # Agar .m4v yoki boshqacha bo'lsa, real mavjud faylni topamiz
            p = Path(filename)
            if not p.exists():
                # Ko‘p hollarda mergedan keyin .mp4 bo'ladi
                alt = p.with_suffix(".mp4")
                if alt.exists():
                    p = alt
            return str(p), info

    return await asyncio.to_thread(_download)

async def handle_instagram_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    text = (msg.caption or "") + "\n" + (msg.text or "")
    match = INSTAGRAM_URL_RE.search(text)

    if not match:
        # Faqat Instagram linklarida ishlaymiz
        return

    url = match.group(0)
    await msg.chat.send_action(ChatAction.UPLOAD_VIDEO)

    with tempfile.TemporaryDirectory() as tmpd:
        tmp = Path(tmpd)
        try:
            file_path_str, info = await _run_yt_dlp(url, tmp, COOKIES_FILE)
            file_path = Path(file_path_str)

            if not file_path.exists():
                await msg.reply_text("Video topilmadi yoki yuklab bo'lmadi. Linkni tekshirib qayta yuboring.")
                return

            size = file_path.stat().st_size
            max_bytes = MAX_MB * 1024 * 1024
            if size > max_bytes:
                await msg.reply_text(
                    f"Video juda katta: { _human_size(size) }. Limit: ~{MAX_MB}MB.\n"
                    f"Iltimos, linkni sifatini past variantga o'zgartirib yuboring yoki qisqaroq videoni tanlang."
                )
                return

            # Sarlavha
            title = info.get("title") or "Instagram Video"
            caption = f"{title}\n\nYuklangan: {_human_size(size)}"

            # Video jo'natish
            with open(file_path, "rb") as f:
                await msg.reply_video(video=f, caption=caption)

        except Exception as e:
            await msg.reply_text(
                "Kechirasiz, yuklashda xatolik yuz berdi. "
                "Agar post private bo'lsa, cookies bilan qayta urinib ko'ring yoki boshqa link yuboring.\n"
                f"Xatolik: {e}"
            )

async def fallback_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Boshqa matn kelsa, foydalanuvchiga yo'l-yo'riq
    await update.message.reply_text("Instagram havolasini yuboring (post yoki reels). Masalan:\nhttps://www.instagram.com/reel/XXXXXXXX/")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))

    # URL bo'lgan har qanday xabarlar
    app.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, handle_instagram_url))

    # Fallback
    app.add_handler(MessageHandler(filters.ALL, fallback_text))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
