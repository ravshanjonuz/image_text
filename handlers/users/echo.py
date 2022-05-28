import pytesseract
from PIL import Image
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

texts = {}

btns = {
    "eng": "🇺🇸 English",
    "rus": "🇷🇺 Russian",
    "uzb_cyrl": "🇺🇿 Uzbek Cyrillic",
    "ukr": "🇺🇦 Ukrainian",
    "kor": "🇰🇷 Korean",
    "kir": "🇰🇬 Kyrgyz",
    "kaz": "🇰🇿 Kazakh",
    "jpn": "🇯🇵 Japan",
    "hin": "🇮🇳 Indian",
    "chi_tra": "🇨🇳 Chinese Traditional",
    "chi_sim": "🇨🇳 Chinese – Simplified",
    "ara": "🇸🇦 Arabic"
    # "Arabic": "🇦🇪 Arabic large"
}


@dp.callback_query_handler()
async def callback_query(call: types.CallbackQuery):
    cid = call.message.chat.id
    try:
        await call.answer()
        if call.data in list(btns.keys()):
            text = pytesseract.image_to_string(Image.open(f"data/images/{cid}.png"), lang=call.data,
                                               config=tessdata_dir_config)

            # text = pytesseract.image_to_string(image)
            await call.message.reply(text) if text else await call.message.reply("Textni ololmadim!")

    except Exception as e:
        print("Query: ", e)


def getBtns():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(btns["eng"], callback_data="eng"),
             InlineKeyboardButton(btns["rus"], callback_data="rus")],
            [InlineKeyboardButton(btns["uzb_cyrl"], callback_data="uzb_cyrl"),
             InlineKeyboardButton(btns["ukr"], callback_data="ukr")],
            [InlineKeyboardButton(btns["kor"], callback_data="kor"),
             InlineKeyboardButton(btns["kir"], callback_data="kir")],
            [InlineKeyboardButton(btns["kaz"], callback_data="kaz"),
             InlineKeyboardButton(btns["jpn"], callback_data="jpn")],
            [InlineKeyboardButton(btns["hin"], callback_data="hin"),
             InlineKeyboardButton(btns["chi_tra"], callback_data="chi_tra")],
            [InlineKeyboardButton(btns["chi_sim"], callback_data="chi_sim"),
             InlineKeyboardButton(btns["ara"], callback_data="ara")]
            # [InlineKeyboardButton(btns["Arabic"], callback_data="Arabic")],
        ]
    )


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def bot_echo(message: types.Message):
    path = f"data/images/{message.chat.id}.png"
    await message.photo[-1].download(path)
    await message.copy_to(message.chat.id, reply_markup=getBtns())
