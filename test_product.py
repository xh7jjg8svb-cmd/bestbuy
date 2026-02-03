import pytest
from products import Product


def test_create_valid_product():
    """Test, dass das Erstellen eines normalen Produkts funktioniert."""
    p = Product("MacBook Air M2", price=1450, quantity=100)
    assert p.name == "MacBook Air M2"
    assert p.price == 1450
    assert p.quantity == 100
    assert p.is_active() is True


def test_create_invalid_product_empty_name():
    """Test, dass ein leerer Name eine Ausnahme auslöst."""
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_create_invalid_product_negative_price():
    """Test, dass ein negativer Preis eine Ausnahme auslöst."""
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_when_quantity_zero():
    """Test, dass ein Produkt inaktiv wird, wenn die Menge 0 erreicht."""
    p = Product("Test Product", price=10, quantity=1)
    p.buy(1)
    assert p.is_active() is False
    assert p.get_quantity() == 0


def test_buy_reduces_quantity_and_returns_correct_total():
    """Test, dass der Kauf die Menge verringert und den korrekten Preis liefert."""
    p = Product("Bose Headphones", price=100, quantity=10)
    total = p.buy(2)
    assert total == 200
    assert p.get_quantity() == 8


def test_buy_more_than_available_raises_exception():
    """Test, dass beim Kauf von mehr als verfügbar eine Ausnahme ausgelöst wird."""
    p = Product("Google Pixel", price=500, quantity=5)
    with pytest.raises(Exception):
        p.buy(10)
