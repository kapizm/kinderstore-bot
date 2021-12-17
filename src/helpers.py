from datetime import datetime

import requests

from src import config


def get_check_data_from_api(check_number: str):
    base_url = config.API_BASE_URL
    headers = {'Authorization': f'Basic {config.API_TOKEN}'}
    json = requests.get(
        base_url + f'/checks/{check_number}', headers=headers,
    ).json()

    return {
        'price': json['price'],
        'registered_at': datetime.strptime(
            json['created_at'], '%d.%m.%Y',
        ),
    }
    # with httpx.Client(
    #     base_url=config.API_BASE_URL,
    #     headers={'Authorization': f'Basic {config.API_TOKEN}'},
    #     max_redirects=0,
    # ) as client:
    #     response = client.get(f'/checks/{check_number}')
    #     print(response.text)

    #     if response.status_code != httpx.codes.OK:
    #         print(response.status_code)
    #         return

    #     json = response.json()
    #     return {
    #         'price': json['price'],
    #         'registered_at': datetime.strptime(
    #             json['created_at'], '%d.%m.%Y',
    #         ),
    #     }


def get_chances_from_price(price: int) -> int:
    if int(price) < 25_000:
        return 0

    price -= 25_000
    chances = 1

    while price >= 20_000:
        chances += 1
        price -= 20_000

    return chances


def get_price(check_number: int) -> int:
    return get_check_data_from_api(check_number)['price']
