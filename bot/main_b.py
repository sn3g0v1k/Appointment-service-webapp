import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Filter, CommandObject, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from config import ADMIN_ID, WEBAPP_URL, BOT_TOKEN
from database import add_new, create_db


# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) == str(ADMIN_ID)



def keyboard_f(user_idd):
    inline_kb_list = [
        [InlineKeyboardButton(text="Веб приложение", web_app=WebAppInfo(url=WEBAPP_URL+f"?tg_id={user_idd}"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # id = str(message.from_user.id)
    # photo = await message.bot.get_user_profile_photos(message.from_user.id, 0, 1)
    # try:
    #     photo_id = photo.photos[0][0].file_id
    # except IndexError:
    #     new_user(conn, cursor, name=message.from_user.full_name, id=id,
    #              url="https://ach-raion.gosuslugi.ru/netcat_files/9/260/MUZhChINA_2.jpg")
    #     await message.answer(f"Hello, {message.from_user.full_name}", reply_markup=keyboard(id))
    #     return
    # url = profile_photo(photo_id, TOKEN)
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=keyboard_f(message.from_user.id))


@dp.message(Command("add_new_specialist"), IsAdmin())
async def refund_command(message: Message, command: CommandObject):
    try:
        args = command.args.split(", ")
        specialist = args[0]
        service = args[1]
        time = args[2]
        client_id = args[3]
        is_busy = args[4]
        date = args[5]
        week_day = args[6]
        add_new(specialist, service, time, client_id, is_busy, date, week_day) # /add_new_specialist Артем Кириешков, стрижка овец, 8:00, None, N, 07.03.2025, friday
        #
        await message.answer("Запись успешно добавлена!")
    except Exception as e:
        print('error', e)

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    create_db()
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
