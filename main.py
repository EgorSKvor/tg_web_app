from config import TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.web_app_info import WebAppInfo

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class AnketStates(StatesGroup):
    wait_fio = State()
    wait_city = State()
    wait_time = State()


@dp.message_handler(text='Привет')
async def hello_func(message: Message):
    await message.answer(text=f'Привет, {message.from_user.first_name}')


@dp.message_handler(commands='anket')
async def start_anket(message: Message):
    await message.answer(text=f'Введите ФИО')
    await AnketStates.wait_fio.set()


@dp.message_handler(state=AnketStates.wait_fio)
async def get_fio(message: Message, state: FSMContext):
    data = await state.get_data()
    data['fio'] = message.text
    await state.update_data(data)
    await message.answer(text=f'Введите город')
    await AnketStates.wait_city.set()


@dp.message_handler(state=AnketStates.wait_city)
async def get_city(message: Message, state: FSMContext):
    data = await state.get_data()
    data['city'] = message.text
    await message.answer(text=f'Введите время')
    await AnketStates.wait_time.set()


@dp.message_handler(state=AnketStates.wait_time)
async def get_city(message: Message, state: FSMContext):
    data = await state.get_data()
    data['time'] = message.text
    print(data)
    await message.answer(text=f'Успешно\n{data}')
    await state.reset_state()


@dp.message_handler(commands='start')
async def start_web_app(message: Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(
        text='Открыть страницу анкеты', web_app=WebAppInfo(url='https://egorskvor.github.io')))
    await message.answer(text='Жми кнопку', reply_markup=markup)


@dp.message_handler(content_types=['web_app_data'])
async def get_data_from_web(message: Message):
    print(message.web_app_data.data, type(message.web_app_data.data))
    await message.answer(message.web_app_data.data)
if __name__ == '__main__':
    executor.start_polling(dp)
