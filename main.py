from aiogram import Bot, Dispatcher, executor, types
import asyncio

API_TOKEN = ""

async def start():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    
    #Создаём инлайн-клавиатуру
    menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
    menu_keyboard.add(
        types.InlineKeyboardButton("Раздел 1", callback_data="section_1"),
        types.InlineKeyboardButton("Раздел 2", callback_data="section_2"),
        types.InlineKeyboardButton("Раздел 3", callback_data="section_3")
    )

    @dp.message_handler(commands = ["start"])
    async def send_welcome(message: types.Message):
        await message.reply("Привет! Я бот!")


    @dp.message_handler(commands = ["help"])
    async def send_menu(message: types.Message):
        await message.reply("Выберите раздел:", reply_markup=menu_keyboard)

    @dp.callback_query_handler(lambda c: c.data.startwith("section_"))
    async def process_menu_selection(callback_query: types.CallbackQuery):
        section = callback_query.data.split("_")[1]
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f"Вы выбрали раздел {section}")

        

    @dp.message_handler()
    async def on_message(message: types.Message):
        await bot.send_message(message.chat.id, message.text)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())
