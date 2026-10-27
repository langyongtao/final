from datetime import datetime

class Item:
    """Represents a class for an individual item """
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

    @property
    def subtotal(self):
        """Calculate the subtotal for this item"""
        return self.price * self.quantity


class ReceiptManager:
    """Receipt Generation and Printing Control Class """
    TAX_RATE = 0.10  # 10% GST 消费税

    def __init__(self):
        self.current_items = []

    def add_item(self, name, price, quantity):
        """Add a new item to the current bill"""
        item = Item(name, price, quantity)
        self.current_items.append(item)
        print(f"✅ Added: {name} x {quantity} (Subtotal: ${item.subtotal:.2f})")

    def calculate_totals(self):
        """Calculate the total amount and taxes"""
        subtotal_sum = sum(item.subtotal for item in self.current_items)
        tax = subtotal_sum * self.TAX_RATE
        total = subtotal_sum + tax
        return subtotal_sum, tax, total

    def print_receipt(self):
        """Print neatly formatted digital receipts to the console (Advanced topic: string alignment and formatting)"""
        if not self.current_items:
            print("\n📭 No items currently purchased！")
            return

        subtotal_sum, tax, total = self.calculate_totals()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n" + "=" * 45)
        print("              Simple POS Electronic Receipt")
        print(f" time: {now_str}")
        print("=" * 45)
        print(f"{'Product Name':<15} | {'price':<8} | {'quantity':<4} | {'Subtotal':<8}")
        print("-" * 45)

        for item in self.current_items:
            print(f"{item.name:<15} | ${item.price:<7.2f} | {item.quantity:<4} | ${item.subtotal:<7.2f}")

        print("-" * 45)
        print(f"{'Item Subtotal:':<30} ${subtotal_sum:>8.2f}")
        print(f"{'GST (10% GST):':<30} ${tax:>8.2f}")
        print(f"{'Total Amount Payable:':<30} ${total:>8.2f}")
        print("=" * 45 + "\n")

    def clear_current(self):
        """Clear the current bill and prepare for the next customer."""
        self.current_items = []
        print("  Shopping cart cleared; new orders can now be entered.！")


# ---------------- 主程序入口 ----------------
def main():
    manager = ReceiptManager()

    while True:
        print("\n" + "=" * 40)
        print("       POS Terminal Electronic Receipt System")
        print("=" * 40)
        print("[1] Add items to the current bill")
        print("[2] Check out and print receipt")
        print("[3] Start a new order (clear current shopping cart)")
        print("[4] exit system")
        print("=" * 40)

        choice = input("Please select an action (1-4): ").strip()

        if choice == "1":
            name = input("Enter product name: ").strip()
            if not name:
                print("⚠️ Product name cannot be empty！")
                continue

            try:
                price = float(input("Enter the unit price of the item ($): "))
                quantity = int(input("Enter purchase quantity: "))
                if price < 0 or quantity <= 0:
                    print("⚠️ The unit price cannot be negative, and the quantity must be greater than 0！")
                    continue
                manager.add_item(name, price, quantity)
            except ValueError:
                print("⚠️ Input format error; unit price and quantity must be numeric.！")

        elif choice == "2":
            manager.print_receipt()

        elif choice == "3":
            manager.clear_current()

        elif choice == "4":
            print("  System exited. Thank you for using it.！")
            break
        else:
            print("❌ Invalid option; please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()