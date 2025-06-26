import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Filter, CommandObject, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from parse import profile_photo
from config import ADMIN_ID, WEBAPP_URL, BOT_TOKEN
from database import add_new, create_db, get_user_appointments, save_user_picture_and_nickname

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log'
)
logger = logging.getLogger(__name__)

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) == str(ADMIN_ID)



async def keyboard_f(user_idd, message):
    photo = await message.bot.get_user_profile_photos(message.from_user.id, 0, 1)
    try:
        photo_id = photo.photos[0][0].file_id
        url = profile_photo(photo_id, BOT_TOKEN)
    except IndexError:
        url="https://avatars.fastly.steamstatic.com/dc77aa1e255492658605e8981ab7d0f4de6cc245_medium.jpg"
    save_user_picture_and_nickname(user_idd, url, message.from_user.full_name)
    inline_kb_list = [
        [InlineKeyboardButton(text="📅 Записаться", web_app=WebAppInfo(url=WEBAPP_URL+f"?tg_id={user_idd}"))],
        [InlineKeyboardButton(text="📋 Мои записи", callback_data="my_appointments")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # try:
        await message.answer(
            f"👋 Привет, {html.bold(message.from_user.full_name)}!\n\n"
            "Я бот для записи к специалистам. С моей помощью вы можете:\n"
            "📅 Записаться на прием\n"
            "📋 Просмотреть свои записи\n"
            "❓ Получить информацию о специалистах",
            reply_markup= await keyboard_f(message.from_user.id, message)
        )
    # except Exception as e:
    #     logger.error(f"Ошибка при обработке команды /start: {str(e)}")
    #     await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

@dp.message(Command("add_new_specialist"), IsAdmin())
async def add_specialist_command(message: Message, command: CommandObject):
    try:
        if not command.args:
            await message.answer(
                "Использование: /add_new_specialist специалист, услуга, время, id_клиента, занятость, дата, день_недели, цена за услугу\n"
                "Пример: /add_new_specialist Артем Кириешков, стрижка овец, 8:00, None, N, 07.03.2025, fridayб 5000"
            )
            return

        args = command.args.split(", ")
        if len(args) != 7:
            await message.answer("Неверное количество аргументов. Нужно 8 аргументов.")
            return

        specialist, service, time, client_id, is_busy, date, week_day, price = args
        add_new(specialist, service, time, client_id, is_busy, date, week_day, price)
        await message.answer("✅ Специалист успешно добавлен!")
    except Exception as e:
        logger.error(f"Ошибка при добавлении специалиста: {str(e)}")
        await message.answer(f"❌ Произошла ошибка при добавлении записи. {str(e)}")

@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/my_appointments - Показать мои записи\n\n"
        "Для записи к специалисту нажмите кнопку 'Записаться'"
    )
    await message.answer(help_text, reply_markup= await keyboard_f(message.from_user.id, message))

@dp.message(Command("my_appointments"))
async def my_appointments_command(message: Message):
    try:
        appointments = get_user_appointments(message.from_user.id)
        if not appointments:
            await message.answer("У вас пока нет записей.")
            return

        response = "📋 Ваши записи:\n\n"
        for app in appointments:
            response += (
                f"👤 Специалист: {app['specialist']}\n"
                f"🕒 Время: {app['time']}\n"
                f"📅 Дата: {app['date']}\n"
                f"🔧 Услуга: {app['service']}\n\n"
            )
        await message.answer(response)
    except Exception as e:
        logger.error(f"Ошибка при получении записей: {str(e)}")
        await message.answer("Произошла ошибка при получении записей.")


@dp.callback_query(lambda a: a.data=="my_appointments")
async def my_appointments_command(query: CallbackQuery):
    try:
        appointments = get_user_appointments(query.from_user.id)
        if not appointments:
            await query.message.answer("У вас пока нет записей.")
            return

        response = "📋 Ваши записи:\n\n"
        for app in appointments:
            response += (
                f"👤 Специалист: {app['specialist']}\n"
                f"🕒 Время: {app['time']}\n"
                f"📅 Дата: {app['date']}\n"
                f"🔧 Услуга: {app['service']}\n\n"
            )
        await query.message.answer(response)
    except Exception as e:
        logger.error(f"Ошибка при получении записей: {str(e)}")
        await query.message.answer("Произошла ошибка при получении записей.")

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer(
            "Я не понимаю эту команду. Используйте /help для просмотра доступных команд.",
            reply_markup=await keyboard_f(message.from_user.id, message)
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {str(e)}")

async def main() -> None:
    try:
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        create_db()
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Критическая ошибка в боте: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
