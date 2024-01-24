# Функция которая сравнивает введёную карту пользователем и карту загадонную компьютером
def is_card(user_card: str, secret_card: str, id: str) -> bool:
    if user_card.split()[0].lower() == secret_card[id]["secret_card"][1] and user_card.split()[1] == secret_card[id]["secret_card"][0][1]:
        return True
    return False
