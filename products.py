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

