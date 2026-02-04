"""Module defining the Product class representing an item in the store."""


class Product:
    """Represents a product with name, price, and quantity."""

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initialize a Product instance.

        Args:
            name (str): Name of the product.
            price (float): Price per unit (must be non-negative).
            quantity (int): Available quantity in stock (must be non-negative).

        Raises:
            ValueError: If name is empty or price/quantity is negative.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True  # Products are active by default

    def get_quantity(self) -> int:
        """Return the current quantity of the product."""
        return self.quantity

    def set_quantity(self, quantity: int):
        """
        Update the product quantity.

        Args:
            quantity (int): New quantity (must be non-negative).

        Raises:
            ValueError: If quantity is negative.
        """
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

    def show(self):
        """Print product details in a readable format."""
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity: int) -> float:
        """
        Purchase a given quantity of this product.

        Args:
            quantity (int): Number of units to buy.

        Returns:
            float: Total price for the purchase.

        Raises:
            Exception: If product is inactive or stock is insufficient.
            ValueError: If quantity <= 0.
        """
        if not self.active:
            raise Exception("Product is inactive and cannot be purchased.")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than 0.")
        if quantity > self.quantity:
            raise Exception("Not enough stock available.")

        total_price = self.price * quantity
        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return total_price
