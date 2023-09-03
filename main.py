from config import TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.web_app_info import WebAppInfo
from table_funcs import to_csv
import time

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


@dp.message_handler(commands=['start'])
async def hi_message(message: Message):
    time.sleep(3)
    await message.answer(text=f'Уже совсем скоро ты попадёшь на мероприятие, которое станет одним из лучших дней твоей жизни.\n\nПервое, о чем бы хотелось сказать, что мероприятие строго для студентов Инженерной академии. Мы любим все факультеты, но отпраздновать хотим конкретно с вами!\n\nЖдём тебя по адресу … к этому времени …')
    time.sleep(5)
    await message.answer(text=f'Мы хотим сделать так, чтобы все прошло идеально и не было никаких казусов. Давайте создадим нечто действительно стоящее и отдохнем без стресса! Поэтому хотелось бы заранее обговорить все правила.\n\nПРЕДУПРЕЖДАЕМ:\n\n⁃ МЕРОПРИЯТИЕ СТРОГО 18+\n⁃ За нанесение ущерба оборудованию и прочему имуществу возложена система штрафов. \n⁃ Мы не несём ответственности за потерянные вещи.\n⁃ Вход строго по спискам.\n⁃ За всем будет следить команда организаторов и охрана. Помимо этого, стоит помнить о наличии камер, которые будут везде. \n⁃ За несоблюдение правил поведения, охрана имеет полное право вывести вас с мероприятия. \n\nЗАПРЕЩЕНЫ: \n\n⁃ Драки.\n⁃ Холодные и огнестрельные оружия.\n⁃ Свой алкоголь.\n⁃ Нарушение дисциплинарного порядка.\n⁃ Наличие запрещенных веществ. \n⁃ Курение сигарет на территории пространства (кроме электронных сигарет и электронных систем для нагревания табака).\n⁃ Проход в зону бара, стола диджея и VIP-зоны для организаторов.')
    time.sleep(10)
    await message.answer(text=f'ЧТО ТЕБЯ ЖДЁТ? \n\n⁃ FREEBAR и закуски (всё входит в стоимость билета). На баре будет представлено меню.\n⁃ Крутая, интерактивная программа с танцами и весельем. \n⁃ Хорошее настроение, новые знакомства и просто крутая тусовка!')
    time.sleep(5)
    await message.answer(text=f'ЧТО ПО ОПЛАТЕ?\n\nСтоимость билета 1500₽. Перевод по реквизитам.\n\n!! В случае исключения с мероприятия из-за нарушения правил пребывания - возврат средств не предусмотрен.')
    time.sleep(5)
    await message.answer(text=f'Дорогие студенты!\n\nЖелаем вам провести время с удовольствием, отдохнуть и получить большое количество ярких и классных эмоций! Ждём тебя 16.09.2023.')


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
    # print(to_table(content))
    to_csv(content)
    await message.answer(message.web_app_data.data)
if __name__ == '__main__':
    executor.start_polling(dp)
