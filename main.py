from random import choice
from os import getenv
from dotenv import load_dotenv, find_dotenv
from telebot import TeleBot


# Загрузка токена из переменной окружения
load_dotenv(find_dotenv())
TOKEN: str = getenv("TOKEN")
# Создаем объект бота
bot = TeleBot(TOKEN)
# Значения номера карты и масти
CARD_NUMBER: list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "В", "Д", "К", "Т"]
CARD_SUIT: list = ["Ч", "Б", "К", "П"]
# Количество попыток, доступных пользователю в игре
ATTEMPTS = 3
# Словарь, в котором будут храниться данные пользователя
users: dict = {}


# Функция возвращающая случайную карту
def get_random_card():
    random_number: str = choice(CARD_NUMBER)
    random_suit: str = choice(CARD_SUIT)
    if random_suit in ["Ч", "Б"]:
        return [f"{random_number}{random_suit}", "красная"]
    return [f"{random_number}{random_suit}", "черная"]


# Этот хэндлер будет срабатывать на команду "/start"
@bot.message_handler(commands=["start"])
def process_start(message):
    bot.send_message(
        message.from_user.id,
        f'Приветствую тебя {message.from_user.first_name}. Это игра "Красная или черная".\n'
        f'Для того чтобы начать игру введи слово "Начало".\n'
        f"С правилами игры можешь ознакомиться введя /help.\n",
    )

    if message.from_user.id not in users:
        users[message.from_user.id] = {
            "in_game": False,
            "secret_card": None,
            "attempts": None,
            "wins": 0,
            "total_games": 0,
        }


# Этот хэндлер будет срабатывать на команду "/help"
@bot.message_handler(commands=["help"])
def process_help(message):
    bot.send_message(
        message.from_user.id,
        f'Правила игра "Красная или черная":\n'
        f"Бот загадывает карту Ваша задача отгдать цвет масти и масть.\n"
        f"Формат ввода ответа: цвет масть."
        f"Количество попыток: {ATTEMPTS}"
        f'Для запуска игры введите "Начало".\n'
        f"Для выхода из игры введите /cancel.\n"
        f"Для вывода своей статистики введите /stat.\n",
    )


# Этот хэндлер будет срабатывать на команду "/stat"
@bot.message_handler(commands=["stat"])
def process_stat(message):
    bot.send_message(
        message.from_user.id,
        f"Ваша статистика игр:\n"
        f"Количество побед: {users[message.from_user.id]['wins']}\n"
        f"Количество сыгранных игр: {users[message.from_user.id]['total_games']}\n",
    )


# Этот хэндлер будет срабатывать на команду "/cancel"
@bot.message_handler(commands=["cancel"])
def process_cancel(message):
    if users[message.from_user.id]["in_game"]:
        users[message.from_user.id]["in_game"] = False
        bot.send_message(
            message.from_user.id,
            f"Вы вышли из игры.\n"
            f"Возвращайтесь ко мне когда захотите снова сыграть.",
        )
    else:
        bot.send_message(
            message.from_user.id,
            f"А мы и так с Вами не играем.\n" f'Введите "Начало" чтобы начать играть.',
        )


# Этот хэндлер будет срабатывать на отправку пользователем запроса на начало игры
@bot.message_handler(func=lambda message: message.text.lower() == "начало")
def process_begin(message):
    if not users[message.from_user.id]["in_game"]:
        users[message.from_user.id]["in_game"] = True
        users[message.from_user.id]["secret_card"] = get_random_card()
        users[message.from_user.id]["attempts"] = ATTEMPTS
        bot.send_message(
            message.from_user.id,
            f"Начнём нашу игру, я загадал карту.\n"
            f"Количество попыток - {ATTEMPTS}.\n"
            f"Введите цвет и масть через пробел.",
        )
    else:
        bot.send_message(
            message.from_user.id, f"Мы и так с Вами играем в игру введите цвет."
        )


# Этот хэндлер будет срабатывать на отправку пользователем цвета и масти карты.
@bot.message_handler(
    func=lambda message: message.text
    and message.text.split()[0].lower() in ["красная", "черная"]
    and message.text.split()[1] in CARD_SUIT
)
def process_game(message):
    if users[message.from_user.id]["in_game"]:
        check_win = False
        if (
            message.text.split()[0].lower()
            == users[message.from_user.id]["secret_card"][1]
            and message.text.split()[1]
            == users[message.from_user.id]["secret_card"][0][1]
        ):
            users[message.from_user.id]["in_game"] = False
            users[message.from_user.id]["wins"] += 1
            users[message.from_user.id]["total_games"] += 1
            users[message.from_user.id]["attempts"] -= 1
            check_win = True
            bot.send_message(
                message.from_user.id,
                f"Ура!! Это верный ответ.\n"
                f"Количество использованных попыток - {ATTEMPTS - users[message.from_user.id]['attempts']}.",
            )
        else:
            users[message.from_user.id]["attempts"] -= 1
            bot.send_message(
                message.from_user.id,
                f"Это не верный ответ.\n"
                f"Количество оставшихся попыток - {users[message.from_user.id]['attempts']}.",
            )
        if users[message.from_user.id]["attempts"] == 0 and not check_win:
            users[message.from_user.id]["in_game"] = False
            users[message.from_user.id]["total_games"] += 1
            bot.send_message(
                message.from_user.id,
                f"К сожалению у вас не получилось отгадать цвет и масть.\n"
                f"Правильный ответ {users[message.from_user.id]['secret_card'][1]} {users[message.from_user.id]['secret_card'][0][1]}\n"
                f'Для старта новой игры введите "Начало".',
            )
    else:
        bot.send_message(message.from_user.id, "Мы еще не играем.")


# Этот хэндлер будет срабатывать на остальные любые сообщения
@bot.message_handler()
def other_process(message):
    if users[message.from_user.id]["in_game"]:
        bot.send_message(
            message.from_user.id, f"Это что такое.\n" f"Введите цвет и масть."
        )
    else:
        bot.send_message(
            message.from_user.id,
            f"Мы ещё не играем.\n" f'Для начала игры введите "Начало".',
        )


if __name__ == "__main__":
    bot.infinity_polling()
