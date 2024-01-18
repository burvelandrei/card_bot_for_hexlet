from random import choice
from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
TOKEN: str = getenv("TOKEN")
CARD_NUMBER: list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т' ]
CARD_SUIT: list = ['Ч', 'Б', 'К', 'П']



