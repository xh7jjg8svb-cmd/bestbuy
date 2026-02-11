"""Module defining Product classes and Promotions for the store."""

from abc import ABC, abstractmethod


class Product:
    """Represents a basic product in the store."""

    def __init__(self, name: str, price: float, quantity: int):
        if not name or not isinstance(name, str):
            raise ValueError("Product name must be a non-empty string.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True
        self.promotion = None

    def get_quantity(self) -> int:
        """Return the quantity of the product."""
        return self.quantity

    def set_quantity(self, quantity: int):
        """Set the product quantity and deactivate if it reaches zero."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Return whether the product is active."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def set_promotion(self, promotion):
        """Assign a promotion to this product."""
        self.promotion = promotion

    def get_promotion(self):
        """Return the current promotion assigned to this product."""
        return self.promotion

    def show(self):
        """Print a readable summary of the product."""
        base = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            base += f", Promotion: {self.promotion.name}"
        print(base)

    def buy(self, quantity: int) -> float:
        """Buy a given quantity of this product, applying promotion if set."""
        if not self.active:
            raise Exception("Product is inactive and cannot be purchased.")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than 0.")
        if quantity > self.get_quantity():
            raise Exception("Not enough stock available.")

        total_price = (
            self.promotion.apply_promotion(self, quantity)
            if self.promotion
            else self.price * quantity
        )

        self.quantity -= quantity
        if self.quantity <= 0:
            self.deactivate()

        return total_price


class NonStockedProduct(Product):
    """A product type that does not have limited stock (e.g., digital goods)."""

    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)

    def get_quantity(self):
        """Return 0 since non-stocked products do not count toward total stock."""
        return 0

    def buy(self, quantity: int) -> float:
        """Buy a non-stocked product."""
        if not self.active:
            raise Exception("Product is inactive and cannot be purchased.")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than 0.")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def show(self):
        """Print information for non-stocked products."""
        base = f"{self.name}, Price: {self.price} (Non-stocked product)"
        if self.promotion:
            base += f", Promotion: {self.promotion.name}"
        print(base)


class LimitedProduct(Product):
    """A product that has a maximum quantity allowed per order."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        if maximum <= 0:
            raise ValueError("Maximum must be greater than 0.")
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        """Buy a limited product respecting the maximum purchase limit."""
        if quantity > self.maximum:
            raise Exception(f"Maximum order quantity for {self.name} is {self.maximum}.")
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = super().buy(quantity)

        self.quantity -= quantity
        if self.quantity <= 0:
            self.deactivate()

        return total_price

    def show(self):
        """Print information about a limited product."""
        base = (
            f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, "
            f"Maximum per order: {self.maximum}"
        )
        if self.promotion:
            base += f", Promotion: {self.promotion.name}"
        print(base)


class Promotion(ABC):
    """Abstract base class for all promotions."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        """Apply the promotion and return the total price."""
        pass


class PercentDiscount(Promotion):
    """Promotion that applies a percentage discount."""

    def __init__(self, name: str, percent: float):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        total = product.price * quantity
        discount = total * (self.percent / 100)
        return total - discount


class SecondHalfPrice(Promotion):
    """Promotion where every second item is half price."""

    def apply_promotion(self, product, quantity: int) -> float:
        full_price_qty = quantity // 2 + quantity % 2
        half_price_qty = quantity // 2
        return (full_price_qty * product.price) + (half_price_qty * product.price * 0.5)


class ThirdOneFree(Promotion):
    """Promotion where every third item is free."""

    def apply_promotion(self, product, quantity: int) -> float:
        groups_of_three = quantity // 3
        remaining = quantity % 3
        total_qty_to_pay = quantity - groups_of_three
        return total_qty_to_pay * product.price
