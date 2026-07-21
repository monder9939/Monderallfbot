import os
import telebot
from yt_dlp import YoutubeDL

# قراءة التوكن بأمان من السيرفر السحابي
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8932503266:AAH3440W_itK7n5b56pxEBowWnTDUILVwGk")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🚀 أهلاً بك في البوت السريع! أرسل لي رابط الفيديو وسأحضره لك فوراً وبأقل استهلاك للوقت.")

@bot.message_handler(func=lambda message: True)
def quick_download_and_send(message):
    url = message.text
    
    if not (url.startswith('http://') or url.startswith('https://')):
        bot.reply_to(message, "❌ يرجى إرسال رابط صحيح.")
        return

    status_msg = bot.reply_to(message, "⚡ جاري جلب الفيديو بأقصى سرعة...")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True, 
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            video_url = info.get('url') or info.get('requested_formats')[0].get('url')
            video_title = info.get('title', 'فيديو')

            bot.send_video(
                message.chat.id, 
                video_url, 
                caption=f"✅ {video_title}\n\nتم التجهيز بسرعـة فائقة 🚀"
            )
            
            bot.delete_message(message.chat.id, status_msg.message_id)

    except Exception as e:
        print(f"Error: {str(e)}")
        bot.edit_message_text(f"❌ عذراً، لم نتمكن من جلب الفيديو بسرعة. تأكد أن الرابط عام وصحيح.", message.chat.id, status_msg.message_id)

if __name__ == "__main__":
    print("🚀 تم تشغيل البوت بنظام السرعة الفائقة الحصري...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

