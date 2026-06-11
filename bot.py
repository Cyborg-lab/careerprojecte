import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8759140245:AAGonSqG4Q7PmtM-p2MyQmo7x20zOzUvEAA"
CHANNEL_ID = -1003625516239

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# 🔘 Category keyboard
category_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="SUV"), KeyboardButton(text="Sedan")],
        [KeyboardButton(text="Pickup"), KeyboardButton(text="Xetchbek")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 📌 FSM State
class CarForm(StatesGroup):
    category = State()
    year = State()
    brand = State()
    model = State()
    price = State()
    email = State()
    phone = State()
    image = State()

# 🚀 START
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Assalomu alaykum 👋\nAutoHub elon berishga hush kelibsiz 🚗\n\nCategory tanlang:",
        reply_markup=category_kb
    )
    await state.set_state(CarForm.category)

@dp.message(CarForm.category)
async def category_handler(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Mashina yilini kiriting 📅:")
    await state.set_state(CarForm.year)

@dp.message(CarForm.year)
async def year_handler(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    await message.answer("Brand kiriting (masalan BMW):")
    await state.set_state(CarForm.brand)

@dp.message(CarForm.brand)
async def brand_handler(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await message.answer("Model kiriting:")
    await state.set_state(CarForm.model)

@dp.message(CarForm.model)
async def model_handler(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Narx kiriting 💰:")
    await state.set_state(CarForm.price)

@dp.message(CarForm.price)
async def price_handler(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Email kiriting 📧:")
    await state.set_state(CarForm.email)

@dp.message(CarForm.email)
async def email_handler(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Telefon raqam kiriting 📞:")
    await state.set_state(CarForm.phone)

@dp.message(CarForm.phone)
async def phone_handler(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Endi mashina rasmini yuboring 📸:")
    await state.set_state(CarForm.image)

@dp.message(F.photo, CarForm.image)
async def image_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_file_id = message.photo[-1].file_id  # eng yuqori sifatli rasm

    text = f"""
🚗 Yangi e'lon!

📂 Category: {data['category']}
📅 Yil: {data['year']}
🏷 Brand: {data['brand']}
🚘 Model: {data['model']}
💰 Narx: {data['price']}
📧 Email: {data['email']}
📞 Telefon: {data['phone']}
"""

    await bot.send_photo(CHANNEL_ID, photo=photo_file_id, caption=text)
    await message.answer("✅ E'loningiz kanalga yuborildi!")

    await state.clear()

@dp.message(CarForm.image)
async def not_photo(message: Message):
    await message.answer("Iltimos, mashina rasmini yuboring 📸")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 