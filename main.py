from random import choice
from os import getenv
from dotenv import load_dotenv, find_dotenv
from telebot import TeleBot



load_dotenv(find_dotenv())
TOKEN: str = getenv("TOKEN")
CARD_NUMBER: list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т' ]
CARD_SUIT: list = ['Ч', 'Б', 'К', 'П']
bot = TeleBot(TOKEN)
users: dict = {}


def get_random_card():
    random_number: str = choice(CARD_NUMBER)
    random_suit: str = choice(CARD_SUIT)
    return f"{random_number}{random_suit}"


@bot.message_handler(commands=['start'])
def process_start(message):
    bot.send_message(message.from_user.id,
        f"Приветствую тебя {message.from_user.first_name}. Это игра \"Красное или черное\".\n"
        f"Для того чтобы начать игру введи слово \"Начало\".\n"
        f"С правилами игры можешь ознакомиться введя /help.\n")

    if message.from_user.id not in users:
        users[message.from_user.id] = {
            "in_game": False,
            "secret_card": None,
            "wins": 0,
            "total_game": 0
            }

@bot.message_handler(commands=['help'])
def process_help(message):
    bot.send_message(message.from_user.id,
        f"Правила игра \"Кравсное или черное\":\n"
        f"Бот загадывает карту Ваша задача отгдать цвет масти.\n"
        f"Для запуска игры введите \"Начало\". Для выхода из игры введите \"Конец\".\n"
        f"Для вывода своей статистики введите /stat.\n")

@bot.message_handler(commands=['stat'])
def process_stat(message):
    bot.send_message(message.from_user.id,
        f"Ваша статистика игр:\n"
        f"Количество побед: {users[message.from_user.id]['wins']}\n"
        f"Количество сыгранных игр: {users[message.from_user.id]['total_game']}\n")






bot.infinity_polling()