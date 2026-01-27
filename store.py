from typing import List, Tuple
from products import Product


class Store:
    def __init__(self, all_products: List[Product]):
        # Validierung: alle Elemente müssen vom Typ Product sein
        if not all(isinstance(p, Product) for p in all_products):
            raise ValueError("Alle Elemente müssen Instanzen der Klasse Product sein.")
        self.products = all_products

    def add_product(self, product: Product):
        """Fügt ein Produkt zum Store hinzu."""
        if not isinstance(product, Product):
            raise ValueError("Nur Instanzen der Klasse Product können hinzugefügt werden.")
        self.products.append(product)

    def remove_product(self, product: Product):
        """Entfernt ein Produkt aus dem Store."""
        if product in self.products:
            self.products.remove(product)
        else:
            raise ValueError("Produkt nicht im Store gefunden.")

    def get_total_quantity(self) -> int:
        """Gibt die Gesamtmenge aller Produkte im Store zurück."""
        return sum(p.get_quantity() for p in self.products)

    def get_all_products(self) -> List[Product]:
        """Gibt eine Liste aller aktiven Produkte im Store zurück."""
        return [p for p in self.products if p.is_active()]

    def order(self, shopping_list: List[Tuple[Product, int]]) -> float:
        """
        Führt eine Bestellung aus.
        shopping_list ist eine Liste von Tupeln: (Produkt, Menge)
        Gibt den Gesamtpreis der Bestellung zurück.
        """
        total_cost = 0.0

        # Vorabprüfung: reicht der Bestand?
        for product, quantity in shopping_list:
            if not product.is_active():
                raise Exception(f"{product.name} ist nicht aktiv und kann nicht bestellt werden.")
            if quantity > product.get_quantity():
                raise Exception(f"Nicht genügend Bestand für {product.name}. Verfügbar: {product.get_quantity()}.")

        # Wenn alles okay ist, Produkte kaufen
        for product, quantity in shopping_list:
            total_cost += product.buy(quantity)

        return total_cost

