import os
import requests
import instaloader
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

ADMIN_ID = os.getenv("ADMIN")  # O'zingning Telegram ID'ingni shu yerga yoz
TOKEN = os.getenv("TELEGRAM_TOKEN")# Bot tokenini shu yerga yozing
USER_LIMIT = 100000
DAILY_LIMIT = 10
async def limit_berish(update: Update, context: CallbackContext):
    user = update.message.from_user

    # Faqat admin ishlatishi mumkin
    if user.id != ADMIN_ID:
        await update.message.reply_text("❌ Sizda bu komanda uchun ruxsat yo‘q.")
        return
    
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("❌ Foydalanish: /limit_berish <user_id> <limit_soni>")
            return
        
        user_id = int(args[0])
        qoshimcha_limit = int(args[1])
        today = datetime.now().date()
        user_limits = {}

        if os.path.exists("user_limits.txt"):
            with open("user_limits.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 4:
                        uid = int(parts[0])
                        usern = parts[1]
                        name = " ".join(parts[2:-2])
                        count = int(parts[-2])
                        date = datetime.strptime(parts[-1], "%Y-%m-%d").date()
                        user_limits[uid] = (usern, name, count, date)
        
        if user_id in user_limits:
            usern, name, count, date = user_limits[user_id]
            if date == today:
                count -= qoshimcha_limit  # Limitni qayta hisoblaymiz
                if count < 0:
                    count = 0
            else:
                count = 0  # Yangi kun bo‘lsa, noldan boshlanadi
            user_limits[user_id] = (usern, name, count, today)
            
            with open("user_limits.txt", "w", encoding="utf-8") as f:
                for uid, (usern, name, count, date) in user_limits.items():
                    f.write(f"{uid} {usern} {name} {count} {date}\n")
            
            await update.message.reply_text(f"✅ Foydalanuvchi {user_id} uchun limit {qoshimcha_limit} ta oshirildi!")
        else:
            await update.message.reply_text("❌ Bu user_id topilmadi.")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")




if not os.path.exists("counter.txt"):
    with open("counter.txt", "w") as f:
        f.write("0")

if not os.path.exists("user_limits.txt"):
    with open("user_limits.txt", "w") as f:
        f.write("")

def get_next_request_number():
    with open("counter.txt", "r+") as f:
        count = int(f.read().strip())
        if count >= USER_LIMIT:
            return None  # Limit tugagan
        f.seek(0)
        f.write(str(count + 1))
        f.truncate()
    return count + 1


def check_user_limit(user_id, username, first_name, last_name):
    today = datetime.now().date()
    user_limits = {}
    full_name = f"{first_name or ''} {last_name or ''}".strip()
    username = username or "Nomalum"

    # Faylni UTF-8 kodlash bilan ochamiz
    if os.path.exists("user_limits.txt"):
        with open("user_limits.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    uid = int(parts[0])
                    user = parts[1]
                    name = " ".join(parts[2:-2])
                    count = int(parts[-2])
                    date = datetime.strptime(parts[-1], "%Y-%m-%d").date()
                    user_limits[uid] = (user, name, count, date)

    # Agar foydalanuvchi mavjud bo‘lsa
    if user_id in user_limits:
        user, name, count, last_date = user_limits[user_id]
        if last_date == today:
            pass  # Bugun limit o‘zgarmaydi
        else:
            count = 0  # Yangi kun, limit yangilanadi
        user_limits[user_id] = (user, name, count, today)
    else:
        user_limits[user_id] = (username, full_name, 0, today)

    # Yangilangan ma'lumotlarni qayta yozamiz
    with open("user_limits.txt", "w", encoding="utf-8") as f:
        for uid, (user, name, count, date) in user_limits.items():
            f.write(f"{uid} {user} {name} {count} {date}\n")

    return user_limits[user_id][2], max(0, DAILY_LIMIT - user_limits[user_id][2])

import os
from datetime import datetime

def increment_user_limit(user_id, username, first_name, last_name):
    today = datetime.now().date()
    user_limits = {}
    full_name = f"{first_name or ''} {last_name or ''}".strip()
    username = username or "Nomalum"
    
    # Foydalanuvchi limitlarini o‘qish
    if os.path.exists("user_limits.txt"):
        with open("user_limits.txt", "r", encoding="utf-8") as f:  # UTF-8 formatida o‘qiymiz
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    uid = int(parts[0])
                    user = parts[1]
                    name = " ".join(parts[2:-2])
                    count = int(parts[-2])
                    date = datetime.strptime(parts[-1], "%Y-%m-%d").date()
                    user_limits[uid] = (user, name, count, date)
    
    # Foydalanuvchi mavjud bo‘lsa, limitni yangilaymiz
    if user_id in user_limits:
        user, name, count, last_date = user_limits[user_id]
        if last_date == today:
            count += 1  # Agar bugun bo‘lsa, limitni oshiramiz
        else:
            count = 1  # Yangi kun boshlangan bo‘lsa, hisobni yangilaymiz
        user_limits[user_id] = (user, name, count, today)
    else:
        user_limits[user_id] = (username, full_name, 1, today)

    # Yangilangan limitlarni faylga yozamiz
    with open("user_limits.txt", "w", encoding="utf-8") as f:  # "w" rejimida yozamiz
        for uid, (user, name, count, date) in user_limits.items():
            f.write(f"{uid} {user} {name} {count} {date}\n")  # Faylni qayta ochish xatosi bartaraf etildi





def download_instagram_video(url):
    try:
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        if post.is_video:
            video_url = post.video_url
            response = requests.get(video_url)
            if response.status_code == 200:
                return response.content
        return None
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return None
    
def download_instagram_media(url):
    try:
        L = instaloader.Instaloader()
        
        # URLni to'g'ri formatga o'tkazish
        if "share/reel/" in url:
            url = url.replace("share/reel/", "reel/")  # Shortlinkni to'g'ri formatga keltirish
        
        shortcode = url.rstrip('/').split("/")[-1]  # URLdan shortcode olish
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if post.is_video:
            return {"type": "video", "content": requests.get(post.video_url).content}
        else:
            return {"type": "photo", "content": [requests.get(img).content for img in post.get_sidecar_nodes()]} if post.typename == "GraphSidecar" else {"type": "photo", "content": [requests.get(post.url).content]}
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return None

async def handle_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    
    if "instagram.com" in text:
        await update.message.reply_text("⏳ Media yuklanmoqda... Iltimos, kuting.")
        media_url, media_type = download_instagram_media(text)
        
        if media_url:
            if media_type == "video":
                await update.message.reply_video(video=media_url, caption="Sizning Instagram videosi 🎥")
            else:
                await update.message.reply_photo(photo=media_url, caption="Sizning Instagram rasmi 🖼")
        else:
            await update.message.reply_text("❌ Media yuklab olinmadi. Havolani tekshirib, qaytadan yuboring!")
    else:
        await update.message.reply_text("❌ Iltimos, faqat Instagram media havolasini yuboring!")


def save_to_file(user_info, user_id, url, success, request_number):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅ Muvaffaqiyatli" if success else "❌ Muvaffaqiyatsiz"
    log_message = f"👤 {user_info} (ID: {user_id}), 🔗 {url}, 📅 {timestamp}, ⛽ Status: {status}, #️⃣ Ariza: {request_number}"
    
    # Faylga yozish
    with open("baza.txt", "a", encoding='utf-8') as file:
        file.write(log_message + "\n")
    
    # Terminalga chiqarish
    print(log_message)




def log_activity(user, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f"👤 {user.first_name or ''} {user.last_name or ''} @{user.username or 'Nomalum'} (ID: {user.id})"
    log_message = f"{timestamp} - {user_info}: {message}"

    # Logni faylga yozish
    with open("log.txt", "a", encoding='utf-8') as file:
        file.write(log_message + "\n")

    # Terminalga chiqarish
    print(log_message)


async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id  # User ID ni olish
    log_activity(user, "Start bosdi")  # Start bosganini logga yozish

    keyboard = [
        [InlineKeyboardButton("👁️ Limitni ko'rish/olish", callback_data='limit')],
        [InlineKeyboardButton("ℹ️ Biz haqimizda", callback_data='about')],
        [InlineKeyboardButton("📊 Bot statistikasi", callback_data='statistika')],
        [InlineKeyboardButton("👮‍♂️ Adminga bog'lanish", callback_data='admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"*Assalomu alaykum va rohmatullohi va barokatuh!* 🌿\n"
        f"👤 *Hurmatli {user.first_name}*, Botimizga Xush kelibsiz!👋 \n"
        f"🆔 *Raqamingiz:* `{user.id}`\n"
        f"🤖 *Bot yaratuvchisi:* [Husanbek Suyunov](https://husanbek-coder.uz)\n"
        f"📹 *YouTube sahifamizga obuna bo'ling:* [📺 YouTube Kanalimiz](https://www.youtube.com/@it_creative)\n\n"
        f"👤 *Hurmatli {user.first_name}*, Botdan foydalanishni boshlashdan oldin iltimos *👁️ Limitni ko'rish* tugmasini bosing aks xolda bot sizga video yubormaydi!!! \n\n"
        f"♻️ *🤖Botni qayta ishga tushurish uchun* /start *ni bosing:*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    user_id = user.id
    await query.answer()
    
    if query.data == "limit":
        used_limit, remaining_limit = check_user_limit(user_id, user.username, user.first_name, user.last_name)
        await query.message.reply_text(f"👁️ Sizning bugungi foydalangan limitingiz: {used_limit}")
    elif query.data == "about":
        await query.message.reply_text(
            "📌 *Bu bot haqida:*\n"
            "Bu bot Instagram reels videolarini tez va oson yuklab olish uchun yaratilgan. "
            "Bizning maqsadimiz — foydalanuvchilarga eng qulay va tezkor xizmatni taqdim etish. "
            "Botimiz orqali Instagram'dagi istalgan video yoki rasmlarni hech qanday qiyinchiliksiz yuklab olishingiz mumkin.\n\n"
            
            "📌 *Foydalanish bo‘yicha qo‘llanma:*\n"
            "Instagram havolasini yuboring va bot sizga media faylni taqdim etadi.\n"
            "Bot bir kunda xar bitta foydalanuvchi uchun 10 ta video yuklab beraoladi!!\n\n"     

            "🌟 *Bizning kanallar:*\n"
            "📢 *Telegram:* [IT Creative](https://t.me/it_creative_news)\n"
            "📺 *YouTube:* [IT Creative](https://www.youtube.com/@it_creative)\n\n"
            
            "👨‍💻 *Admin bilan bog‘lanish:*\n"
            "🔹 [@husanbek_coder](https://t.me/husanbek_coder)\n"
            "☎️ *Telefon:* +998 97 521 66 86",
            parse_mode="Markdown"
        )

    elif query.data == "admin":
        await query.message.reply_text(
            "📩 *Admin bilan bog‘lanish:*\n\n"
            "👨‍💻 *Telegram:* [@husanbek_coder](https://t.me/husanbek_coder)\n"
            "☎️ *Telefon:* +998 97 521 66 86\n\n"
            "❓ Agar bot ishlamayotgan bo‘lsa yoki savollaringiz bo‘lsa, bemalol yozing.\n\n"
            "🔄 *🤖Botni qayta ishga tushurish uchun:* /start",
            parse_mode="Markdown"
        )
    elif query.data == "statistika":
        await statistikani_korsat(update, context)  # Statistika funktsiyasini chaqirish
    print(f"🔘Inline tugma bosildi: {query.data} | 👤Foydalanuvchi : {user.first_name} ID ({user.id})")  # Debug uchun


async def handle_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    log_activity(user, f"Yozdi: {text}")  # Foydalanuvchi yozganini logga yozish

    if any(word in text.lower() for word in ["salom", "assalom", "salomm"]):
        await update.message.reply_text("Assalom alekom! 😊\nMenga Instagram havola yuboring men sizga Video qilib yuboraman!")
        return
    elif any(word in text.lower() for word in ["rahmat", "raxmat"]):
        await update.message.reply_text("Bizning xizmatlardan foydalanganingiz uchun tashakkur! 😊")
        return
    elif any(word in text.lower() for word in ["qalesan", "qalisan", "qlesan","qaleysan"]):
        await update.message.reply_text("Yaxshi raxmat! 😊\nMenga Instagram havola yuboring men sizga Video qilib yuboraman!")
        return
    elif any(word in text.lower() for word in ["💋"]):
        await update.message.reply_text("😊")
        await update.message.reply_text("His tuyg'ularga berilmang!\nHavola yuboring!")
        return
    elif any(word in text.lower() for word in ["admin"]):
        await update.message.reply_text("Admin bilan bog'lanish uchun:\n@husanbek_coder telegram manzil\n+998 97 521 66 86 A'loqa raqami orqali\nBog'lanishingiz mumkin.\n🤖Botni qayta ishga tushurish uchun /start")
        return
    if "instagram.com" in text:
        used_limit, remaining_limit = check_user_limit(user.id, user.username, user.first_name, user.last_name)
        if used_limit >= DAILY_LIMIT:
            await update.message.reply_text(f"❌ Sizning bugungi xizmat limingiz tugadi. \nLimitlar {used_limit}/{DAILY_LIMIT}\n🤖Botni qayta ishga tushurish uchun /start")
            return
        
        request_number = get_next_request_number()
        if request_number is None:
            await update.message.reply_text("❌ Umumiy xizmat limiti tugagan.\n🤖Botni qayta ishga tushurish uchun /start")
            return

        await update.message.reply_text("⏳ Media yuklanmoqda... \n▶️Iltimos, biroz kuting...\n⏳Bu bir necha soniya vaqt oladi!")
        video_content = download_instagram_video(text)
        if video_content:
            increment_user_limit(user.id, user.username, user.first_name, user.last_name)
            await update.message.reply_video(video=video_content, caption=f"🔗 Havola: {text}\n#️⃣ Ariza raqami: {request_number}\n👁️Sizning qolgan kunlik limitingiz: {remaining_limit - 1}/{DAILY_LIMIT}\n🤖Botni qayta ishga tushurish uchun /start")
            save_to_file(f"{user.first_name or ''} {user.last_name or ''} @{user.username or 'Nomalum'}", user.id, text, True, request_number)
        else:
            save_to_file(f"{user.first_name or ''} {user.last_name or ''} @{user.username or 'Nomalum'}", user.id, text, False, request_number)
            await update.message.reply_text(f"❌ Video yuklab olishda xatolik.\n#️⃣ Ariza raqami: {request_number} ")
    else:
        await update.message.reply_text(f"❌ Iltimos, faqat Instagram video havolasini yuboring.\n🤖Botni qayta ishga tushurish uchun /start")


        
def get_statistics():
    total_users = 100
    total_requests = 100
    today_requests = 100
    successful_requests = 100
    failed_requests = 0
    today = datetime.now().date()

    # Umumiy foydalanuvchilarni hisoblash
    if os.path.exists("log.txt"):
        try:
            with open("log.txt", "r", encoding="utf-8") as log_file:
                start_count = sum(1 for line in log_file if "Start bosdi" in line)
                total_users = start_count  # Faqat "Start bosdi" soniga teng bo'ladi
        except UnicodeDecodeError:
            print("❌ Xatolik: `log.txt` faylini UTF-8 formatida saqlang!")

    # Umumiy so‘rovlar sonini hisoblash
    if os.path.exists("counter.txt"):
        try:
            with open("counter.txt", "r", encoding="utf-8") as f:
                total_requests = int(f.read().strip() or 0)
        except (UnicodeDecodeError, ValueError):
            print("❌ Xatolik: `counter.txt` noto‘g‘ri formatda!")

    # Bugungi muvaffaqiyatli va muvaffaqiyatsiz yuklangan videolarni hisoblash
    if os.path.exists("baza.txt"):
        try:
            with open("baza.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if "📅" in line and "⛽ Status:" in line:
                        parts = line.strip().split(", ")
                        try:
                            date_str = parts[2].split("📅 ")[1].split(" ")[0]
                            status = parts[3].split("⛽ Status: ")[1]
                            log_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                            if log_date == today:
                                today_requests += 1
                                if "✅ Muvaffaqiyatli" in status:
                                    successful_requests += 1
                                else:
                                    failed_requests += 1
                        except (IndexError, ValueError):
                            continue  # Noto'g'ri formatdagi ma'lumotlarni e'tibordan chetda qoldiramiz
        except UnicodeDecodeError:
            print("❌ Xatolik: `baza.txt` faylini UTF-8 formatida saqlang!")

    return total_users, total_requests, today_requests, successful_requests, failed_requests


async def statistikani_korsat(update: Update, context: CallbackContext):
    total_users, total_requests, today_requests, successful_requests, failed_requests = get_statistics()

    statistikalar = (
        "📊 *Bot statistikasi* 📊\n\n"
        f"👤 Umumiy foydalanuvchilar: {total_users}\n"
        f"📥 Jami so‘rovlar: {total_requests}\n"
        f"📅 Bugungi so‘rovlar: {today_requests}\n\n"
        f"✅ Bugun yuklangan muvaffaqiyatli videolar: {successful_requests}\n"
        f"❌ Bugungi muvaffaqiyatsiz yuklamalar: {failed_requests}\n"
    )

    # Callback query javobini jo‘natish (aksi holda bot xato beradi)
    await update.callback_query.answer()

    await update.callback_query.message.edit_text(statistikalar, parse_mode="Markdown")


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"{timestamp} - {message}\n"
    
    # Terminalga chiqaramiz
    print(log_text.strip())

    # Faylga yozamiz
    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(log_text)
    except UnicodeEncodeError:
        print("❌ Xatolik: `log.txt` faylini UTF-8 formatida saqlang!")

import openpyxl

async def foydalanuvchilar_excel(update: Update, context: CallbackContext):
    user = update.message.from_user
    
    # Faqat admin ishlatishi mumkin
    if user.id != ADMIN_ID:
        await update.message.reply_text("❌ Sizda bu komanda uchun ruxsat yo‘q.")
        return
    
    if not os.path.exists("user_limits.txt"):
        await update.message.reply_text("❌ Foydalanuvchi ma'lumotlari topilmadi.")
        return
    
    try:
        # Excel fayl yaratamiz
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Foydalanuvchilar"
        
        # Sarlavhalar
        sheet.append(["User ID", "Username", "Full Name", "Bugungi So‘rovlar", "Sana"])
        
        with open("user_limits.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    uid = int(parts[0])
                    username = parts[1]
                    name = " ".join(parts[2:-2])
                    count = int(parts[-2])
                    date = parts[-1]
                    sheet.append([uid, username, name, count, date])
        
        # Excel faylni saqlash
        filename = "foydalanuvchilar.xlsx"
        workbook.save(filename)
        
        # Faylni adminga yuborish
        await context.bot.send_document(chat_id=user.id, document=open(filename, "rb"))
    
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")


async def latest_news(update: Update, context: CallbackContext):
    user = update.message.from_user
    
    # Faqat admin ishlatishi mumkin
    if user.id != ADMIN_ID:
        await update.message.reply_text("❌ Sizda bu komanda uchun ruxsat yo‘q.")
        return
    
    if not os.path.exists("baza.txt"):
        await update.message.reply_text("❌ Hali hech qanday ma'lumot yo‘q.")
        return
    
    try:
        # Excel fayl yaratamiz
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Oxirgi 50 foydalanuvchi"
        
        # Sarlavhalar
        sheet.append(["User ID", "Ism Familiya", "Username", "Havola", "Sana", "Status"])
        
        # Baza faylidan ma'lumot o‘qish
        with open("baza.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Oxirgi 50 ta yozuvni olish
        last_50 = lines[-50:] if len(lines) > 50 else lines
        
        for line in last_50:
            try:
                # Ma'lumotlarni ajratish
                parts = line.split(", ")
                user_info = parts[0].split(" (ID: ")
                name_username = user_info[0].replace("👤 ", "")
                user_id = user_info[1].split(")")[0]
                
                link = parts[1].replace("🔗 ", "")
                date = parts[2].replace("📅 ", "")
                status = parts[3].replace("⛽ Status: ", "").strip()
                
                username = ""
                if "@" in name_username:
                    name_parts = name_username.split("@")
                    full_name = name_parts[0].strip()
                    username = "@" + name_parts[1].strip()
                else:
                    full_name = name_username.strip()
                
                sheet.append([user_id, full_name, username, link, date, status])
            except:
                continue  # Xato bo'lsa, o'tkazib yuboramiz
        
        # Excel faylni saqlash
        filename = "latest_news.xlsx"
        workbook.save(filename)
        
        # Faylni adminga yuborish
        await context.bot.send_document(chat_id=user.id, document=open(filename, "rb"))
    
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")



def main():
    log_message("🚀 Bot ishlamoqda...")
    application = ApplicationBuilder().token(TOKEN).build() 
    application.add_handler(CommandHandler("limit_berish", limit_berish))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("latest_news", latest_news))
    application.add_handler(CommandHandler("foydalanuvchilar", foydalanuvchilar_excel))
    application.add_handler(CommandHandler("statistika", statistikani_korsat))  
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
if __name__ == '__main__':
    main()