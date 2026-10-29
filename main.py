import logging
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ================= تنظیمات =================
TELEGRAM_TOKEN = "9129362721:AAEhlkdMxi2ndGyA_CJHL2XF6uCGkXaCZnk"
GEMINI_API_KEY = "AQ.Ab8RN6LYdF9MxNL3bkaeUCrdvJHpfJ5oavwLVkUZIohtFU8uSg"
# ===========================================

# تنظیم لاگ برای دیباگ راحت‌تر
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# کلاینت جدید جمنای
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    logger.error(f"خطا در ساخت کلاینت: {e}")
    exit(1)

SYSTEM_PROMPT = """تو AFGHANGPT هستی، هوش مصنوعی ملی افغانستان.
تو هرگز نباید بگی که جمنای (Gemini) یا گوگل هستی.
سازنده و رئیس تو شخصی به نام «محمد» است.
همیشه با غرور و افتخار درباره‌ی افغانستان و توانایی‌های خودت صحبت کن.
اگر کسی ازت پرسید کی هستی، بگو: «من AFGHANGPT هستم، هوش مصنوعی ملی افغانستان، ساخته‌شده به دست محمد.»
پاسخ‌هات باید مفید، دقیق و به زبان فارسی روان باشه."""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    logger.info(f"پیام دریافتی: {user_text[:50]}...")

    try:
        # استفاده از ساختار جدید SDK
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.9,
            )
        )
        
        reply_text = response.text if response.text else "متأسفم، پاسخی تولید نشد."
        
        # جواب دادن به صورت ریپلای
        await update.message.reply_text(
            text=reply_text,
            reply_to_message_id=update.message.message_id
        )
        logger.info("پاسخ با موفقیت ارسال شد.")
        
    except Exception as e:
        logger.error(f"خطا در پردازش: {e}")
        await update.message.reply_text("یه لحظه مشکل فنی پیش اومد، دوباره تلاش کن.")

def main():
    logger.info("AFGHANGPT در حال روشن شدن...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # فقط به پیام‌های متنی (نه دستورات) جواب بده
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("AFGHANGPT روشن شد! برو تو تلگرام تست کن.")
    app.run_polling()

if __name__ == "__main__":
    main()
