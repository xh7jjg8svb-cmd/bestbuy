# products.py

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

    # Produkt anzeigen
    def show(self):
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}")

    # Produkt kaufen
    def buy(self, quantity: int) -> float:
        if not self.active:
            raise Exception("Produkt ist nicht aktiv und kann nicht gekauft werden.")
        if quantity <= 0:
            raise ValueError("Die Kaufmenge muss größer als 0 sein.")
        if quantity > self.quantity:
            raise Exception("Nicht genügend Bestand vorhanden.")

        total_price = self.price * quantity
        self.quantity -= quantity

        # Deaktivieren, falls keine Menge mehr übrig
        if self.quantity == 0:
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
        # Menge auf 0 setzen (wird aber in get_quantity überschrieben)
        super().__init__(name, price, quantity=0)

    def get_quantity(self):
        # Gibt praktisch unendlich zurück, damit Store-Prüfungen bestehen.
        # float('inf') funktioniert gut für Vergleiche (z.B. qty > get_quantity()).
        return float("inf")

    def buy(self, quantity: int) -> float:
        # Verhalten: nicht-lagernde Produkte reduzieren nicht die Menge.
        if not self.active:
            raise Exception("Produkt ist nicht aktiv und kann nicht gekauft werden.")
        if quantity <= 0:
            raise ValueError("Die Kaufmenge muss größer als 0 sein.")

        # Einfacher Rückgabewert: Preis * Menge
        return self.price * quantity

    def show(self):
        # Überschreibe Anzeige, um die besondere Art zu zeigen
        print(f"{self.name}, Price: {self.price} (Non-stocked product)")


class LimitedProduct(Product):
    """
    Produkte mit einer maximalen Bestellmenge pro Bestellung (maximum).
    Beispiel: Versandgebühr, die nur einmal pro Bestellung hinzugefügt werden darf.
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        if maximum <= 0:
            raise ValueError("Das maximum muss größer als 0 sein.")
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        # Zuerst prüfen, ob die gewünschte Menge das Limit pro Bestellung überschreitet
        if quantity > self.maximum:
            raise Exception(f"Maximale Bestellmenge für {self.name} ist {self.maximum}.")
        # Dann das normale Kaufverhalten (prüft auch Bestand, Aktivität etc.)
        return super().buy(quantity)

    def show(self):
        # Überschreibe Anzeige, um die maximale Menge zu zeigen
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum per order: {self.maximum}")
