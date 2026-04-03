import pytest
from shopping import Cart, log_purchase


@pytest.fixture
def cart():
    return Cart()


def test_add_item(cart):
    cart.add_item("Apple", 10.0)
    assert len(cart.items) == 1


def test_add_item_negative_price(cart):
    with pytest.raises(ValueError):
        cart.add_item("Apple", -5.0)


def test_total(cart):
    cart.add_item("Apple", 10.0)
    cart.add_item("Banana", 5.0)
    assert cart.total() == 15.0


@pytest.mark.parametrize(
    "discount, expected",
    [
        (0, 100.0),
        (50, 50.0),
        (100, 0.0),
    ],
)
def test_apply_discount_valid(cart, discount, expected):
    cart.add_item("Item", 100.0)
    cart.apply_discount(discount)
    assert cart.total() == expected


@pytest.mark.parametrize("discount", [-10, 150])
def test_apply_discount_invalid(cart, discount):
    cart.add_item("Item", 100.0)
    with pytest.raises(ValueError):
        cart.apply_discount(discount)


def test_log_purchase(monkeypatch):
    called = {}

    def mock_post(url, json):
        called["url"] = url
        called["json"] = json

    monkeypatch.setattr("shopping.requests.post", mock_post)

    item = {"name": "Apple", "price": 10}
    log_purchase(item)

    assert called["url"] == "https://example.com/log"
    assert called["json"] == item
