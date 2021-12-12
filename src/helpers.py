def get_chances_from_price(price: int) -> int:
    if price < 25_000:
        return 0

    price -= 25_000
    chances = 1

    while price >= 20_000:
        chances += 1
        price -= 20_000

    return chances
