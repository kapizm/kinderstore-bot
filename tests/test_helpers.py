from typing import List

import pytest

from src.helpers import get_chances_from_price, get_total_chances


@pytest.mark.parametrize(
    'price, chances',
    [
        (0, 0),
        (25_000, 1),
        (30_000, 1),
        (45_000, 2),
        (65_000, 3),
    ],
)
def test_get_chances_from_price(price: int, chances: int):
    assert get_chances_from_price(price) == chances


@pytest.mark.parametrize(
    'chances_list, total_chances',
    [
        ([], 0),
        ([1], 1),
        ([1, 0], 1),
        ([0, 0], 0),
        ([1, 1], 2),
    ],
)
def test_get_total_chances(chances_list: List[int], total_chances: int):
    assert get_total_chances(chances_list) == total_chances
