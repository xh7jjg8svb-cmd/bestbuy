"""Module defining the Store class that manages multiple products."""

from typing import List, Tuple
from products import Product


class Store:
    """Represents a store that holds and manages multiple products."""

    def __init__(self, all_products: List[Product]):
        """
        Initialize a Store with a list of Product instances.

        Args:
            all_products (List[Product]): List of products to add to the store.

        Raises:
            ValueError: If any element is not an instance of Product.
        """
        if not all(isinstance(p, Product) for p in all_products):
            raise ValueError("All elements must be instances of Product.")
        self.products = all_products

    def add_product(self, product: Product):
        """
        Add a new product to the store.

        Args:
            product (Product): The product to add.

        Raises:
            ValueError: If argument is not a Product instance.
        """
        if not isinstance(product, Product):
            raise ValueError("Only Product instances can be added.")
        self.products.append(product)

    def remove_product(self, product: Product):
        """
        Remove a product from the store.

        Args:
            product (Product): The product to remove.

        Raises:
            ValueError: If the product is not found in the store.
        """
        if product in self.products:
            self.products.remove(product)
        else:
            raise ValueError("Product not found in store.")

    def get_total_quantity(self) -> int:
        """Return the total quantity of all products in the store."""
        return sum(p.get_quantity() for p in self.products)

    def get_all_products(self) -> List[Product]:
        """Return a list of all active products."""
        return [p for p in self.products if p.is_active()]

    def order(self, shopping_list: List[Tuple[Product, int]]) -> float:
        """
        Process an order from a list of (Product, quantity) tuples.

        Args:
            shopping_list (List[Tuple[Product, int]]): List of products and their quantities.

        Returns:
            float: The total price of the order.

        Raises:
            Exception: If any product is inactive or quantity exceeds available stock.
        """
        total_cost = 0.0

        # Validate stock availability before processing
        for product, quantity in shopping_list:
            if not product.is_active():
                raise Exception(f"{product.name} is inactive and cannot be ordered.")
            if quantity > product.get_quantity():
                raise Exception(
                    f"Not enough stock for {product.name}. "
                    f"Available: {product.get_quantity()}."
                )

        # Process the order
        for product, quantity in shopping_list:
            total_cost += product.buy(quantity)

        return total_cost
