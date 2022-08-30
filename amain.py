import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from filters import IsAdminFilter, IsOwnerFilter

logging.basicConfig(level=logging.INFO)


# init bot
async def on_startup(dp):
    await bot.send_message(config.BOT_OWNER, "BOT_Started"
                                             "\nБот запущен")


storage = MemoryStorage()
bot = Bot(token="5626042316:AAGXx65KiWKOR6tFIgPE8Xl_1yUtnkSRXKI")
dp = Dispatcher(bot, storage=storage)


class predloj(StatesGroup):
    get = State()


class prvideo(StatesGroup):
    video = State()


class prphoto(StatesGroup):
    photo = State()


class praudio(StatesGroup):
    audio = State()


class prdrugoe(StatesGroup):
    drugoe = State()


# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    reply = ReplyKeyboardMarkup(resize_keyboard=True)
    r1 = 'Предложить (фото и т.д)'
    r2 = 'Купить рекламу'
    r3 = 'Связаться с Админом'
    r4 = 'Связаться с Владельцом'
    r6 = 'Наш Чат'
    r7 = 'Купить такого же бота'
    btn1 = "Отмена"
    reply.add(r1, r2, r3, r4, r6, r7)
    reply.insert(btn1)
    await message.answer('Здраствуй, Бот поможет тебе связаться с администраторами⚜️'
                         '\n              Пиши по поводу рекламы♻️'
                         '\n     Если у тебя есть хорошие идеи для канала❗️'
                         '\n      отправь сюда свои идеи, свои варианты👌🏼')
    await message.answer('Ты можешь использовать нужное тебе действие через меню', reply_markup=reply)

@dp.message_handler(commands='delete_b')
async def remove_b(message: types.Message):
    markup = ReplyKeyboardRemove()
    await message.answer('Кнопки удалены', reply_markup=markup)

@dp.message_handler(content_types=['text'])
async def predlojka(message: types.Message):
    if message.text == "Предложить (фото и т.д)":
        reply = ReplyKeyboardMarkup(resize_keyboard=True)
        r1 = "Фото"
        r2 = "Видео"
        r3 = "Музыку"
        r4 = "Другое"
        reply.add(r1, r2, r3, r4)
        await message.answer('Что вы хотите предложить нашему каналу?', reply_markup=reply)
        await predloj.get.set()
    elif message.text == "Купить рекламу":
        inline = InlineKeyboardMarkup()
        inlined = InlineKeyboardButton("Менеджер", url='https://t.me/Abduqodirov_19')
        inline.add(inlined)
        await message.answer("Рекламный", reply_markup=inline)
    elif message.text == "Связаться с Админом":
        inline = InlineKeyboardMarkup(row_width=3)
        inlined = InlineKeyboardButton('Администратора🔰', url='https://t.me/adiljanov_i')
        inline.add(inlined)
        await message.answer('Профиль', reply_markup=inline)
    elif message.text == 'Связаться с Владельцом':
        inline = InlineKeyboardMarkup(row_width=3)
        inlined = InlineKeyboardButton('Владелеца⚜️', url='https://t.me/Rasul1ov')
        inline.add(inlined)
        await message.answer("Профиль", reply_markup=inline)
    elif message.text == "Наш Чат":
        inline = InlineKeyboardMarkup(row_width=3)
        inlined = InlineKeyboardButton('Наш чат 🏠', url='https://t.me/druzya_chatikX')
        inline.add(inlined)
        await bot.send_message(message.chat.id, 'Ссылка', reply_markup=inline)
    elif message.text == 'Купить такого же бота':
        inline = InlineKeyboardMarkup()
        inlined = InlineKeyboardButton("Профиль👨🏻‍💻", url='t.me/theHero_7')
        inline.add(inlined)
        await message.answer('Привет это я @theHero_7 создатель бота'
                             '\n ️Писавший ему код и т.д'
                             '\n Если хочешь такого же бота'
                             '\n Пиши мне в личку '
                             '\n 👇👇👇', reply_markup=inline)
    elif message.text == 'Отмена':
        reply = ReplyKeyboardRemove()
        await message.answer("Закрывается...", reply_markup=reply)

@dp.message_handler(content_types=['text'], state=predloj.get)
async def select_action(message: types.Message, state: FSMContext):
    reply = ReplyKeyboardRemove()
    if message.text == "Фото":
        await message.answer("Отлично, "
                             "\nОтправьте Фотографию", reply_markup=reply)
        await prphoto.photo.set()
    elif message.text == "Видео":
        await message.answer("Отлично,"
                             "\nОтправьте Видео", reply_markup=reply)
        await prvideo.video.set()
    elif message.text == "Музыку":
        await message.answer("Отлично,"
                             "\nОтправьте Музыку", reply_markup=reply)
        await praudio.audio.set()
    elif message.text == "Другое":
        await message.answer("Отлично,"
                             "\nНапишите вашу идею", reply_markup=reply)
        await prdrugoe.drugoe.set()


@dp.message_handler(content_types=['photo'], state=prphoto.photo)
async def photo(message: types.Message, state: FSMContext):
    reply = ReplyKeyboardMarkup(resize_keyboard=True)
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    photo_id = message.photo[-1].file_id
    r1 = "/start"
    reply.add(r1)
    await message.answer('OK'
                         '\nЯ отправил ваше фото Модераторам', reply_markup=reply)
    await bot.send_photo(config.BOT_CHAT, photo_id,
                         caption=f"Это фото было отправлено от {user_id}, {user_name}, @{username}")
    await state.finish()


@dp.message_handler(content_types='video', state=prvideo.video)
async def video(message: types.Message, state: FSMContext):
    reply = ReplyKeyboardMarkup(resize_keyboard=True)
    r1 = "/start"
    reply.add(r1)
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    id_id = message.video.file_id
    await message.answer('OK'
                         '\nЯ отправил ваше видео Модераторам', reply_markup=reply)
    await bot.send_video(config.BOT_CHAT, id_id,
                         caption=f"Это видео было отправлено от {user_id}, {user_name} @{username}")
    await state.finish()


@dp.message_handler(content_types='audio', state=praudio.audio)
async def audio(message: types.Message, state: FSMContext):
    reply = ReplyKeyboardMarkup(resize_keyboard=True)
    r1 = "/start"
    reply.add(r1)
    audio_id = message.audio.file_id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    await message.answer('OK'
                         '\nЯ отправил вашу музыку Модераторам', reply_markup=reply)
    await bot.send_audio(config.BOT_CHAT, audio_id,
                         caption=f"Это музыка было отправлено от {user_id}, {user_name} @{username}")
    await state.finish()


@dp.message_handler(content_types='text', state=prdrugoe.drugoe)
async def drugoe(message: types.Message, state: FSMContext):
    reply = ReplyKeyboardMarkup(resize_keyboard=True)
    r1 = "/start"
    reply.add(r1)
    text = message.text
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    await message.answer("OK"
                         "\nЯ отправил ваше предложение Модераторам", reply_markup=reply)
    await bot.send_message(config.BOT_CHAT, f'Предложение от @{username} {user_id} {user_name}'
                                            f'\n{text}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
