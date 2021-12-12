import pytest

from src.helpers import get_chances_from_price


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
