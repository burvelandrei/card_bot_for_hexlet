from random import choice

# Функция возвращающая случайную карту
def get_random_card(CARD_NUMBER, CARD_SUIT):
    random_number: str = choice(CARD_NUMBER)
    random_suit: str = choice(CARD_SUIT)
    if random_suit in ["Ч", "Б"]:
        return [f"{random_number}{random_suit}", "красная"]
    return [f"{random_number}{random_suit}", "черная"]