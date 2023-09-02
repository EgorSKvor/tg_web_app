from config import TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.web_app_info import WebAppInfo
from table_funcs import to_table

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class AnketStates(StatesGroup):
    wait_fio = State()
    wait_napr = State()
    wait_age = State()
    wait_whyYou = State()


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
    await message.answer(text=f'Введите направление обучения')
    await AnketStates.wait_napr.set()


@dp.message_handler(state=AnketStates.wait_napr)
async def get_napr(message: Message, state: FSMContext):
    data = await state.get_data()
    data['napr'] = message.text
    await message.answer(text=f'Введите дату рождения')
    await AnketStates.wait_age.set()

@dp.message_handler(state=AnketStates.wait_age)
async def get_age(message: Message, state: FSMContext):
    data = await state.get_data()
    data['age'] = message.text
    await message.answer(text=f'Введите время')
    await AnketStates.wait_whyYou.set()


@dp.message_handler(state=AnketStates.wait_whyYou)
async def get_city(message: Message, state: FSMContext):
    data = await state.get_data()
    data['whyYou'] = message.text
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
    content = message.web_app_data.data
    to_table(content)
    await message.answer(message.web_app_data.data)
if __name__ == '__main__':
    executor.start_polling(dp)
