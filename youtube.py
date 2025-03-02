import yt_dlp

url = input("YouTube havolasini kiriting: ")

opts = {
    "format": "bestvideo[height<=720]+bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
}

try:
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
        print("Video muvaffaqiyatli yuklab olindi!")
except Exception as e:
    print(f"Xatolik yuz berdi: {e}")
