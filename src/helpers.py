from datetime import datetime

import httpx

from src import config

def get_check_data_from_api(check_number: str):
    with httpx.Client(
        base_url=config.API_BASE_URL,
        headers={'Authorization': f'Basic {config.API_TOKEN}'},
    ) as client:
        response = client.get(f'/checks/{check_number}')

        if response.status_code != httpx.codes.OK:
            return

        json = response.json()
        return {
            'price': json['price'],
            'registered_at': datetime.strptime(
                json['created_at'], '%d.%m.%Y',
            ),
        }


def get_chances_from_price(price: int) -> int:
    if price < 25_000:
        return 0

    price -= 25_000
    chances = 1

    while price >= 20_000:
        chances += 1
        price -= 20_000

    return chances
