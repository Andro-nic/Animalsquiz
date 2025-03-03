import os
from aiogram import Router, Bot
from aiogram import types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext  # Отслеживания вопроса
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from quiz import questions
import animals
from animals import animal_info
from animals import animal_images
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
#переменные окружения
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
HOST_NAME = os.getenv('HOST_NAME')
PORT = os.getenv('PORT')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
WEBSITE = os.getenv('WEBSITE')


bot = Bot(token=TOKEN)
router = Router()

# глобальные переменные
animals = animals.animals
current_question_index = 0


async def send_main_menu(chat_id: int, state: FSMContext, exclude: list[str] | None = None):

    menu_actions = {
        "start": "Вернуться к старту",
        "info": "Наша цель",
        "share": "Поделиться результатом",
        "feedback": "Обратная связь",
        "restart": "Узнать свой тотем"
    }

    if exclude:
        for action_to_exclude in exclude:
            if action_to_exclude in menu_actions:
                del menu_actions[action_to_exclude]

    # создаём кнопки
    inline_keyboard = [
        [types.InlineKeyboardButton(text=label, callback_data=f"menu:{action}")]
        for action, label in menu_actions.items()
    ]

    markup = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    menu_message = await bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
    await state.update_data(menu_message_id=menu_message.message_id)


# обработчики команд
#/start` отправляет приветственное сообщение и предлагает пользователю начать викторину
@router.message(Command('start', 'help'))
async def start(msg: Message, state: FSMContext):
    user_name = msg.from_user.first_name
    text = f"""Я, <b>манул Тимофей</b> - 
    символ <i>Московского Зоопарка</i>
    
    Привет, {user_name}!!!
    
Я рад, что ты посетил мой телеграмм бот. 
            
Сегодня я проведу для тебя викторину,               
цель которой подобрать тебе тотемное животное.
Для этого тебе нужно нажать на кнопку
'Узнать свой тотем' и честно отвечать на вопросы.

Хочешь пройти викторину, жми - "Узнать свой тотем"
Хочешь узнать про нашем проекте, - жми "Наша цель" 
 """

    await bot.send_photo(msg.chat.id, photo=types.FSInputFile('images/manul.jpg'))
    await bot.send_message(msg.chat.id, text, parse_mode='HTML')
    await send_main_menu(msg.chat.id, state, exclude=["start", "share",'feedback'])

#/info` предоставляет информацию о проекте Московского зоопарка
@router.message(Command('info'))
async def info(msg: Message, state: FSMContext):

    text = f"""
Основная цель Московского зоопарка — сохранение биоразнообразия планеты.
Участие в программе «Клуб друзей зоопарка» — это помощь в содержании наших обитателей. 
В настоящее время опекуны объединились в неформальное сообщество — Клуб друзей Московского зоопарка. 
Опекать – значит помогать любимым животным.
Подробнее о программе опеки вы можете узнать на нашем сайте или позвонив по телефону:

📞 Телефон: <a href="tel:{PHONE_NUMBER}">{PHONE_NUMBER}</a>'
   
🌐 Вебсайт: <a href="{WEBSITE}">{WEBSITE}</a>
"""

    await bot.send_photo(msg.chat.id, photo=types.FSInputFile('images/MZoo-logo-hor-rus-preview-RGB.jpg'))
    await bot.send_message(msg.chat.id, text=text, parse_mode='HTML')
    await send_main_menu(msg.chat.id, state, exclude=["info","share",'feedback'])

#/share` позволяет пользователю поделиться своим тотемным животным
@router.message(Command('share'))
async def share_result(msg: Message, state: FSMContext):
    data = await state.get_data()
    if 'animals' in data:
        result = max(data['animals'], key=data['animals'].get)
        file_path = animal_images.get(result)
        print(animal_images)
        if file_path:  # Проверяем, есть ли файл для животного
            photo = FSInputFile(file_path)  # Создаем объект FSInputFile для локального файла
            await bot.send_photo(
                msg.chat.id,
                photo,
                caption=(
                    'Поделись изображением в мессенджере - помоги остальным узнать о "Клубе друзей".\n\n'
                    f'Мое тотемное животное: {result}\n\n'
                    f'Присоединяйся к нашему боту: {BOT_USERNAME}'
                )
            )
        else:
            await bot.send_message(msg.chat.id, f"Изображение для '{result}' не найдено.")

    await send_main_menu(msg.chat.id, state, exclude=["share"])


#feedback` позволяет пользователю получить обратную связь, отправив электронное письмо.
@router.message(Command('feedback'))
async def get_feedback(msg: Message, state: FSMContext):
    data = await state.get_data()
    print(data)

    # отправляем номер телефона пользователю
    await bot.send_message(
        msg.chat.id,
        f'Наш контактный номер: <a href="tel:{PHONE_NUMBER}">{PHONE_NUMBER}</a>',
        parse_mode='HTML'
    )

    # получаем данные о пользователе и результате
    user_name = msg.from_user.username
    result = max(data['animals'], key=data['animals'].get)

    # формируем текст письма
    email_subject = "Викторина: отзыв пользователя"
    email_body = f"Имя пользователя: {user_name}\n" \
                 f"Номер телефона: {PHONE_NUMBER}\n" \
                 f"Тотемное животное: {result}"

    # отправляем письмо
    try:
        message = MIMEMultipart()
        message['From'] = EMAIL_ADDRESS
        message['To'] = RECIPIENT_EMAIL
        message['Subject'] = email_subject
        message.attach(MIMEText(email_body, 'plain'))

        # настройка SMTP соединения
        await aiosmtplib.send(
            message,
            hostname=HOST_NAME,
            port=PORT,
            username=EMAIL_ADDRESS,
            password=EMAIL_PASSWORD,
            #use_tls=True
        )
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")

    await send_main_menu(msg.chat.id, state, exclude=["feedback"])


#/restart` очищает состояние и перезапускает викторину.
@router.message(Command('restart'))
async def restart(msg: Message, state: FSMContext):
    await state.clear()
    await quiz(msg, state)


class QuizState(StatesGroup):
    waiting_for_answer = State()


# управление логикой викторины
@router.message(Command('quiz'))
async def quiz(msg: Message, state: FSMContext):
    await state.update_data(current_question_index=0,
                            animals={animal: 0 for animal in animals.keys()})
    await send_question(msg.chat.id, state, msg)


async def send_question(chat_id: int, state: FSMContext, msg: Message):
    data = await state.get_data()
    current_question_index = data.get('current_question_index', 0)
    if current_question_index < len(questions):
        question = questions[current_question_index]
        # создание кнопок викторины
        inline_keyboard_buttons = [
            [types.InlineKeyboardButton(text=option, callback_data=f"answer:{option}")]
            for option in question['options']
        ]
        inline_markup = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard_buttons)
        # удаляем предыдущее сообщение с вопросом
        question_message_id = data.get('question_message_id')
        if question_message_id:
            try:
                await bot.delete_message(chat_id, question_message_id)
            except Exception:
                pass
        # новый вопрос
        sent_message = await bot.send_message(chat_id, question['question'], reply_markup=inline_markup)

        await state.update_data(question_message_id=sent_message.message_id)
        # ожидания ответа
        await state.set_state(QuizState.waiting_for_answer)
    else:
        await show_result(chat_id, state, msg)


@router.callback_query(lambda c: c.data.startswith("answer:"))
async def handle_inline_answer(callback_query: types.CallbackQuery, state: FSMContext):
    selected_option = callback_query.data.split(":")[1]
    # получаем данные состояния
    data = await state.get_data()
    current_question_index = data.get('current_question_index', 0)
    if current_question_index < len(questions):
        question = questions[current_question_index]

        for animal in question['animal_mapping'].get(selected_option, []):
            data['animals'][animal] = data['animals'].get(animal, 0) + 1
        # обновляем состояние
        await state.update_data(current_question_index=current_question_index + 1, animals=data['animals'])
        # удаляем сообщение с кнопками
        try:
            await callback_query.message.delete()
        except Exception as e:
            pass
        # переходим к следующему вопросу
        await send_question(callback_query.message.chat.id, state, callback_query.message)
    else:
        await show_result(callback_query.message.chat.id, state, callback_query.message)  # !!!


@router.callback_query(lambda c: c.data.startswith("menu:"))
async def handle_menu_callback(callback_query: types.CallbackQuery, state: FSMContext):
    action = callback_query.data.split("menu:")[1]

    # Удаляем текущее меню
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        try:
            await bot.delete_message(callback_query.message.chat.id, menu_message_id)
        except Exception:
            pass

    # Вызываем соответствующую команду
    if action == "start":
        await start(callback_query.message, state)
    elif action == "info":
        await info(callback_query.message, state)
    elif action == "share":
        await share_result(callback_query.message, state)
    elif action == "feedback":
        await get_feedback(callback_query.message, state)
    elif action == "restart":
        await restart(callback_query.message, state)
    # Закрываем всплывающее уведомление Telegram
    await callback_query.answer()


# обрабатываем результат, добавляем информацию о животном и отправляем пользователю.
async def show_result(chat_id: int, state: FSMContext, msg: Message):
    data = await state.get_data()
    result = max(data['animals'], key=data['animals'].get)

    await bot.send_message(chat_id, f'Твое тотемное животное - <b>{result}</b>! ', parse_mode='HTML')

    await animal_info(chat_id, result)
    await send_main_menu(msg.chat.id, state)