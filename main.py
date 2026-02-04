"""Main entry point for running the store management system."""

import products
import store


def start(best_buy):
    """
    Display the main menu for the store application.

    Args:
        best_buy (store.Store): The store instance to operate on.
    """
    while True:
        print("\n--- Store Menu ---")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose an option (1-4): ")

        if choice == "1":
            print("\nAvailable Products:")
            all_products = best_buy.get_all_products()
            for i, p in enumerate(all_products, 1):
                print(f"{i}. ", end="")
                p.show()

        elif choice == "2":
            total = best_buy.get_total_quantity()
            print(f"\nTotal items in store: {total}")

        elif choice == "3":
            make_order(best_buy)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


def make_order(best_buy):
    """
    Facilitate creating a customer order by selecting products and quantities.

    Args:
        best_buy (store.Store): The store from which to order products.
    """
    all_products = best_buy.get_all_products()
    shopping_list = []

    print("\nStarting an order. Enter product number and amount (or leave blank to finish).")

    while True:
        for i, p in enumerate(all_products, 1):
            print(f"{i}) {p.name} (Price: {p.price}, Stock: {p.quantity})")

        prod_idx = input("Product number: ")
        if not prod_idx:
            break

        amount = input("Amount: ")
        if not amount:
            break

        try:
            idx = int(prod_idx) - 1
            qty = int(amount)

            selected_product = all_products[idx]
            shopping_list.append((selected_product, qty))
            print("Added to cart.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid numbers.")

    if shopping_list:
        try:
            total_price = best_buy.order(shopping_list)
            print(f"Order successful! Total price: {total_price}")
        except Exception as e:
            print(f"Order failed: {e}")


# Setup initial inventory
product_list = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250),
]

best_buy = store.Store(product_list)

if __name__ == "__main__":
    start(best_buy)
