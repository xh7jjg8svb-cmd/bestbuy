"""Module defining the Store class that manages products and orders."""

from typing import List, Tuple
from products import Product


class Store:
    """Represents a store that manages a collection of products."""

    def __init__(self, all_products: List[Product]):
        if not all(isinstance(p, Product) for p in all_products):
            raise ValueError("All elements must be instances of Product.")
        self.products = all_products

    def add_product(self, product: Product):
        """Add a product to the store."""
        if not isinstance(product, Product):
            raise ValueError("Only Product instances can be added.")
        self.products.append(product)

    def remove_product(self, product: Product):
        """Remove a product from the store."""
        if product in self.products:
            self.products.remove(product)
        else:
            raise ValueError("Product not found in store.")

    def get_total_quantity(self) -> int:
        """Return the total quantity of all stocked (physical) products."""
        total = 0
        for p in self.products:
            q = p.get_quantity()
            if q != float("inf"):
                total += q
        return total

    def get_all_products(self) -> List[Product]:
        """Return a list of all active products."""
        return [p for p in self.products if p.is_active()]

    def order(self, shopping_list: List[Tuple[Product, int]]) -> float:
        """
        Execute an order and return the total cost.

        Args:
            shopping_list (List[Tuple[Product, int]]): List of (Product, quantity) tuples.

        Returns:
            float: The total cost of the order.
        """
        total_cost = 0.0

        # Pre-check availability
        for product, quantity in shopping_list:
            if not product.is_active():
                raise Exception(f"{product.name} is inactive and cannot be ordered.")
            if quantity > product.get_quantity():
                raise Exception(
                    f"Not enough stock for {product.name}. "
                    f"Available: {product.get_quantity()}."
                )

        # If all checks pass, execute the purchase
        for product, quantity in shopping_list:
            total_cost += product.buy(quantity)

        return total_cost
