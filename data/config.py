from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

CHANNELS = ['-1001571981540']

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
btn_accept = "✅ A'zo bo'ldim"
text_notaccepted = "❌<b> Kanalga a'zo bo'lmadingiz</b>, iltimos botdan foydalanish uchun kanalga a'zo bo'ling!"
text_accepted = "<b>Tabriklaymiz ✅,</b> Siz muvaffaqiyatli roʻyxatdan oʻtdingiz!"
text_request_text = "🙂 Botdan to'liq va <b>BEPUL</b> foydalanish uchun telegram kanalimizga a'zo bo'ling!"
