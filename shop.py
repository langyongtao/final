import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# ==================== 1. 数据模型 ====================
class Item:
    """商品数据模型"""

    def __init__(self, name, price, quantity=1, category="General"):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.category = category

    @property
    def subtotal(self):
        return self.price * self.quantity


# ==================== 2. GUI 主程序 ====================
class POSApp:
    TAX_RATE = 0.10  # 10% GST

    def __init__(self, root):
        self.root = root
        self.root.title("🛒 POS Terminal & Electronic Receipt System")
        self.root.geometry("1100x680")
        self.root.minsize(900, 600)

        # 预设英文商品列表 (配合澳洲老师的餐饮/咖啡场景)
        self.products = [
            {"name": "☕ Flat White", "price": 4.50, "category": "Beverages"},
            {"name": "🧋 Iced Milk Tea", "price": 5.50, "category": "Beverages"},
            {"name": "🥐 Butter Croissant", "price": 3.80, "category": "Bakery"},
            {"name": "🍰 Tiramisu", "price": 6.50, "category": "Desserts"},
            {"name": "🥪 Chicken Burger", "price": 9.90, "category": "Mains"},
            {"name": "🍕 Italian Pizza", "price": 12.50, "category": "Mains"},
            {"name": "🥤 Coke Zero", "price": 2.50, "category": "Beverages"},
            {"name": "🍦 Vanilla Sundae", "price": 3.00, "category": "Desserts"},
        ]

        # 当前购物车列表: {商品名: Item对象}
        self.cart = {}

        # 配置 UI 样式
        self.setup_styles()
        # 构建界面布局
        self.create_widgets()

    def setup_styles(self):
        """配置整体视觉主题风格"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure('TFrame', background='#F3F4F6')

        # 按钮样式
        self.style.configure('Action.TButton', font=('Segoe UI', 10, 'bold'), background='#2563EB', foreground='white')
        self.style.map('Action.TButton', background=[('active', '#1D4ED8')])

        self.style.configure('Success.TButton', font=('Segoe UI', 10, 'bold'), background='#10B981', foreground='white')
        self.style.map('Success.TButton', background=[('active', '#059669')])

        self.style.configure('Danger.TButton', font=('Segoe UI', 10, 'bold'), background='#EF4444', foreground='white')
        self.style.map('Danger.TButton', background=[('active', '#DC2626')])

    def create_widgets(self):
        """主窗口组件布局"""
        # 顶部标题栏
        header_frame = tk.Frame(self.root, bg="#1E293B", height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🛍️ POS Terminal Electronic Receipt System",
            font=("Segoe UI", 16, "bold"),
            bg="#1E293B",
            fg="#FFFFFF"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # 主内容区域（双面板结构）
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # ==================== 左侧：商品挑选区 (Store Center) ====================
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # 1. 手动添加商品条（输入框区域）
        custom_input_frame = tk.LabelLabelFrame if hasattr(tk, 'LabelLabelFrame') else tk.LabelFrame
        custom_input_frame = tk.LabelFrame(left_frame, text=" ➕ Manual Entry / Quick Add ",
                                           font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#374151", padx=10, pady=10)
        custom_input_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))

        tk.Label(custom_input_frame, text="Name:", bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(custom_input_frame, width=14)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(custom_input_frame, text="Price($):", bg="#FFFFFF").grid(row=0, column=2, padx=5, pady=5)
        self.entry_price = ttk.Entry(custom_input_frame, width=8)
        self.entry_price.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(custom_input_frame, text="Qty:", bg="#FFFFFF").grid(row=0, column=4, padx=5, pady=5)
        self.entry_qty = ttk.Entry(custom_input_frame, width=6)
        self.entry_qty.insert(0, "1")
        self.entry_qty.grid(row=0, column=5, padx=5, pady=5)

        add_btn = ttk.Button(custom_input_frame, text="Add to Cart", style='Action.TButton',
                             command=self.add_custom_item)
        add_btn.grid(row=0, column=6, padx=10, pady=5)

        # 2. 商品点餐网格区 (快捷点击卡片)
        product_section = tk.LabelFrame(left_frame, text=" 🏪 Quick Select Menu ", font=("Segoe UI", 10, "bold"),
                                        bg="#FFFFFF", fg="#374151", padx=10, pady=10)
        product_section.pack(fill=tk.BOTH, expand=True)

        grid_frame = tk.Frame(product_section, bg="#FFFFFF")
        grid_frame.pack(fill=tk.BOTH, expand=True)

        cols = 3
        for i, prod in enumerate(self.products):
            row = i // cols
            col = i % cols

            card = tk.Frame(grid_frame, bg="#F8FAFC", highlightbackground="#E2E8F0", highlightthickness=1, bd=0)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            lbl_name = tk.Label(card, text=prod["name"], font=("Segoe UI", 11, "bold"), bg="#F8FAFC", fg="#1E293B")
            lbl_name.pack(anchor="w", padx=10, pady=(10, 2))

            lbl_price = tk.Label(card, text=f"${prod['price']:.2f}", font=("Segoe UI", 10), bg="#F8FAFC", fg="#2563EB")
            lbl_price.pack(anchor="w", padx=10, pady=(0, 8))

            btn_add = tk.Button(
                card,
                text="+ Add",
                font=("Segoe UI", 9, "bold"),
                bg="#3B82F6",
                fg="white",
                relief="flat",
                cursor="hand2",
                command=lambda p=prod: self.quick_add_product(p)
            )
            btn_add.pack(fill=tk.X, padx=10, pady=(0, 10))

        for c in range(cols):
            grid_frame.columnconfigure(c, weight=1)

        # ==================== 右侧：购物车与结账 (Cart & Checkout) ====================
        right_frame = tk.LabelFrame(main_container, text=" 🛒 Order Details & Checkout ", font=("Segoe UI", 10, "bold"),
                                    bg="#FFFFFF", fg="#374151", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        right_frame.config(width=420)

        columns = ("name", "price", "qty", "subtotal")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=12)

        self.tree.heading("name", text="Product Name")
        self.tree.heading("price", text="Price")
        self.tree.heading("qty", text="Qty")
        self.tree.heading("subtotal", text="Subtotal")

        self.tree.column("name", width=130, anchor="w")
        self.tree.column("price", width=70, anchor="e")
        self.tree.column("qty", width=50, anchor="center")
        self.tree.column("subtotal", width=80, anchor="e")

        self.tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 金额汇总区域
        summary_frame = tk.Frame(right_frame, bg="#F8FAFC", padx=15, pady=10)
        summary_frame.pack(fill=tk.X, pady=(0, 10))

        self.lbl_subtotal = tk.Label(summary_frame, text="Subtotal: $0.00", font=("Segoe UI", 10), bg="#F8FAFC",
                                     anchor="w")
        self.lbl_subtotal.pack(fill=tk.X, pady=2)

        self.lbl_tax = tk.Label(summary_frame, text="GST (10%): $0.00", font=("Segoe UI", 10), bg="#F8FAFC", anchor="w")
        self.lbl_tax.pack(fill=tk.X, pady=2)

        self.lbl_total = tk.Label(summary_frame, text="Total Amount: $0.00", font=("Segoe UI", 13, "bold"),
                                  fg="#DC2626", bg="#F8FAFC", anchor="w")
        self.lbl_total.pack(fill=tk.X, pady=4)

        # 底部控制按钮组
        btn_frame = tk.Frame(right_frame, bg="#FFFFFF")
        btn_frame.pack(fill=tk.X)

        btn_clear = ttk.Button(btn_frame, text="Clear Cart", style='Danger.TButton', command=self.clear_cart)
        btn_clear.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        btn_checkout = ttk.Button(btn_frame, text="Checkout & Print", style='Success.TButton', command=self.checkout)
        btn_checkout.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

    # ==================== 3. 业务逻辑操作 ====================
    def quick_add_product(self, prod):
        name = prod["name"]
        price = prod["price"]

        if name in self.cart:
            self.cart[name].quantity += 1
        else:
            self.cart[name] = Item(name, price, 1, prod.get("category", "General"))

        self.update_cart_ui()

    def add_custom_item(self):
        name = self.entry_name.get().strip()
        price_str = self.entry_price.get().strip()
        qty_str = self.entry_qty.get().strip()

        if not name:
            messagebox.showwarning("Warning", "⚠️ Product name cannot be empty!")
            return

        try:
            price = float(price_str)
            qty = int(qty_str)
            if price < 0 or qty <= 0:
                messagebox.showwarning("Warning", "⚠️ Price cannot be negative and quantity must be greater than 0!")
                return

            if name in self.cart:
                self.cart[name].quantity += qty
            else:
                self.cart[name] = Item(name, price, qty, "Custom")

            self.entry_name.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.entry_qty.insert(0, "1")

            self.update_cart_ui()

        except ValueError:
            messagebox.showerror("Error", "⚠️ Invalid input format! Price and quantity must be numbers.")

    def update_cart_ui(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        subtotal_sum = 0.0
        for item in self.cart.values():
            self.tree.insert("", tk.END, values=(
                item.name,
                f"${item.price:.2f}",
                item.quantity,
                f"${item.subtotal:.2f}"
            ))
            subtotal_sum += item.subtotal

        tax = subtotal_sum * self.TAX_RATE
        total = subtotal_sum + tax

        self.lbl_subtotal.config(text=f"Subtotal: ${subtotal_sum:.2f}")
        self.lbl_tax.config(text=f"GST (10%): ${tax:.2f}")
        self.lbl_total.config(text=f"Total Amount: ${total:.2f}")

    def clear_cart(self):
        if not self.cart:
            return
        if messagebox.askyesno("Confirmation", "Are you sure you want to clear the shopping cart?"):
            self.cart.clear()
            self.update_cart_ui()

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Notice", "📭 The shopping cart is empty. Please add items first!")
            return

        subtotal_sum = sum(item.subtotal for item in self.cart.values())
        tax = subtotal_sum * self.TAX_RATE
        total = subtotal_sum + tax
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 生成英文格式的小票
        receipt_text = f"{'=' * 42}\n"
        receipt_text += f"{'Simple POS Electronic Receipt':^42}\n"
        receipt_text += f" Time: {now_str}\n"
        receipt_text += f"{'=' * 42}\n"
        receipt_text += f"{'Product Name':<14} | {'Price':<7} | {'Qty':<4} | {'Subtotal':<7}\n"
        receipt_text += f"{'-' * 42}\n"

        for item in self.cart.values():
            receipt_text += f"{item.name:<12} | ${item.price:<6.2f} | {item.quantity:<4} | ${item.subtotal:<6.2f}\n"

        receipt_text += f"{'-' * 42}\n"
        receipt_text += f"{'Item Subtotal:':<26} ${subtotal_sum:>8.2f}\n"
        receipt_text += f"{'GST (10%):':<26} ${tax:>8.2f}\n"
        receipt_text += f"{'Total Payable:':<26} ${total:>8.2f}\n"
        receipt_text += f"{'=' * 42}\n"
        receipt_text += f"{'Thank you for your visit!':^38}\n"

        self.show_receipt_window(receipt_text)

    def show_receipt_window(self, receipt_content):
        win = tk.Toplevel(self.root)
        win.title("🧾 Electronic Receipt")
        win.geometry("420x520")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        text_area = tk.Text(win, font=("Courier New", 10), bg="#FFFFF0", fg="#000000", padx=15, pady=15)
        text_area.insert(tk.END, receipt_content)
        text_area.config(state=tk.DISABLED)
        text_area.pack(fill=tk.BOTH, expand=True)

        close_btn = ttk.Button(win, text="Complete & New Order", style='Success.TButton',
                               command=lambda: [win.destroy(), self.cart.clear(), self.update_cart_ui()])
        close_btn.pack(fill=tk.X, padx=15, pady=10)


# ==================== 4. 程序主入口 ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()