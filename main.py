from aiogram import Bot, Dispatcher, executor, types
import asyncio

API_TOKEN = ""

async def start():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands = ["start"])
    async def send_welcome(message: types.Message):
        await message.reply("Привет! Я бот!")

    @dp.message_handler()
    async def on_message(message: types.Message):
        await bot.send_message(message.chat.id, message.text)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())
