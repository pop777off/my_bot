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

    section_1_keyboard = types.InlineKeyboardMarkup()
    section_1_keyboard.add(types.InlineKeyboardButton("Пункт 1", callback_data="section_1_item_1"))
    section_1_keyboard.add(types.InlineKeyboardButton("Пункт 2", callback_data="section_1_item_2"))
    section_1_keyboard.add(types.InlineKeyboardButton("Пункт 3", callback_data="section_1_item_3"))
    section_1_keyboard.add(types.InlineKeyboardButton("Пункт 4", callback_data="section_1_item_4"))

    @dp.message_handler(commands = ["start"])
    async def send_welcome(message: types.Message):
        await message.reply("Привет! Я бот!")


    @dp.message_handler(commands = ["help"])
    async def send_menu(message: types.Message):
        await message.reply("Выберите раздел:", reply_markup=menu_keyboard)

    @dp.callback_query_handler(lambda c: c.data == "section_1")
    async def show_section_1_menu(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Выберите пункт из раздела 1:", reply_markup=section_1_keyboard)

    @dp.callback_query_handler(lambda c: c.data.startswith("section_1_item_"))
    async def process_section_1_selection(callback_query: types.CallbackQuery):
        item = callback_query.data.split("_")[2]
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f"Вы выбрали пункт {item} из раздела 1")

    @dp.callback_query_handler(lambda c: c.data in ["section_2", "section_3"])
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
