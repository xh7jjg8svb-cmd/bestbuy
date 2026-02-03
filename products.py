from abc import ABC, abstractmethod

class Product:
    def __init__(self, name: str, price: float, quantity: int):
        # Validierungen
        if not name or not isinstance(name, str):
            raise ValueError("Produktname darf nicht leer sein.")
        if price < 0:
            raise ValueError("Preis darf nicht negativ sein.")
        if quantity < 0:
            raise ValueError("Menge darf nicht negativ sein.")

        # Instanzvariablen
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True  # Produkte sind standardmäßig aktiv
        self.promotion = None  # keine Aktion standardmäßig

    # Getter für quantity
    def get_quantity(self) -> int:
        return self.quantity

    # Setter für quantity
    def set_quantity(self, quantity: int):
        if quantity < 0:
            raise ValueError("Menge darf nicht negativ sein.")
        self.quantity = quantity
        # Wenn Menge 0 erreicht, wird das Produkt deaktiviert
        if self.quantity == 0:
            self.deactivate()

    # Getter für active
    def is_active(self) -> bool:
        return self.active

    # Produkt aktivieren
    def activate(self):
        self.active = True

    # Produkt deaktivieren
    def deactivate(self):
        self.active = False

    # Getter / Setter für Promotion
    def set_promotion(self, promotion):
        self.promotion = promotion

    def get_promotion(self):
        return self.promotion

    # Produkt anzeigen
    def show(self):
        base = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            base += f", Promotion: {self.promotion.name}"
        print(base)

    # Produkt kaufen
    def buy(self, quantity: int) -> float:
        if not self.active:
            raise Exception("Produkt ist nicht aktiv und kann nicht gekauft werden.")
        if quantity <= 0:
            raise ValueError("Die Kaufmenge muss größer als 0 sein.")
        if quantity > self.get_quantity():
            raise Exception("Nicht genügend Bestand vorhanden.")

        # Preis über Promotion berechnen, falls gesetzt
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity

        # Menge reduzieren nur für physische / lagernde Produkte
        if hasattr(self, "quantity") and self.quantity != float("inf"):
            self.quantity -= quantity
            if self.quantity <= 0:
                self.deactivate()

        return total_price


# -------------------------
# Neue Klassen (Erweiterungen)
# -------------------------

class NonStockedProduct(Product):
    """
    Produkte, die nicht gelagert werden (z. B. Software-Lizenzen).
    Menge wird nicht reduziert; es gibt praktisch unbegrenzte Verfügbarkeit.
    """

    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)

    def get_quantity(self):
        return float("inf")

    def buy(self, quantity: int) -> float:
        if not self.active:
            raise Exception("Produkt ist nicht aktiv und kann nicht gekauft werden.")
        if quantity <= 0:
            raise ValueError("Die Kaufmenge muss größer als 0 sein.")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def show(self):
        base = f"{self.name}, Price: {self.price} (Non-stocked product)"
        if self.promotion:
            base += f", Promotion: {self.promotion.name}"
        print(base)


class LimitedProduct(Product):
    """
    Produkte mit einer maximalen Bestellmenge pro Bestellung (maximum).
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        if maximum <= 0:
            raise ValueError("Das maximum muss größer als 0 sein.")
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise Exception(f"Maximale Bestellmenge für {self.name} ist {self.maximum}.")
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = super().buy(quantity)
            return total_price
        # Menge reduzieren
        if self.quantity != float("inf"):
            self.quantity -= quantity
            if self.quantity <= 0:
                self.deactivate()
        return total_price

    def show(self):
        base = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum per order: {self.maximum}"
        if self.promotion:
            base += f", Promotion: {self.promotion.name}"
        print(base)


# -------------------------
# Promotion Klassen
# -------------------------

class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        pass


class PercentDiscount(Promotion):
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        total = product.price * quantity
        discount = total * (self.percent / 100)
        return total - discount


class SecondHalfPrice(Promotion):
    def apply_promotion(self, product, quantity: int) -> float:
        full_price_qty = quantity // 2 + quantity % 2
        half_price_qty = quantity // 2
        return full_price_qty * product.price + half_price_qty * product.price * 0.5


class ThirdOneFree(Promotion):
    def apply_promotion(self, product, quantity: int) -> float:
        groups_of_three = quantity // 3
        remaining = quantity % 3
        total_qty_to_pay = quantity - groups_of_three
        return total_qty_to_pay * product.price
