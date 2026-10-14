"""
PocketTools — маленький набір корисних інструментів:
  1. Генератор паролів
  2. Конвертер одиниць
  3. Гра «Вгадай число»
"""

import random
import string
import tkinter as tk
from tkinter import ttk


# ---------------------------------------------------------------- Генератор паролів
class PasswordTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        self.length = tk.IntVar(value=12)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        self.password = tk.StringVar()
        self.status = tk.StringVar()

        ttk.Label(self, text="Генератор паролів", style="Title.TLabel").pack(anchor="w")

        row = ttk.Frame(self)
        row.pack(fill="x", pady=(15, 5))
        ttk.Label(row, text="Довжина:").pack(side="left")
        self.len_label = ttk.Label(row, text="12", width=3)
        self.len_label.pack(side="right")
        ttk.Scale(row, from_=4, to=40, variable=self.length,
                  command=self._on_length).pack(side="left", fill="x", expand=True, padx=10)

        ttk.Checkbutton(self, text="Великі літери (A-Z)", variable=self.use_upper).pack(anchor="w", pady=2)
        ttk.Checkbutton(self, text="Цифри (0-9)", variable=self.use_digits).pack(anchor="w", pady=2)
        ttk.Checkbutton(self, text="Символи (!@#$...)", variable=self.use_symbols).pack(anchor="w", pady=2)

        entry = ttk.Entry(self, textvariable=self.password, font=("Consolas", 14), justify="center")
        entry.pack(fill="x", pady=(15, 10), ipady=4)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Згенерувати", command=self.generate).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(buttons, text="Скопіювати", command=self.copy).pack(side="left", expand=True, fill="x", padx=(5, 0))

        ttk.Label(self, textvariable=self.status, foreground="green").pack(pady=10)

        self.generate()

    def _on_length(self, value):
        self.length.set(int(float(value)))
        self.len_label.config(text=str(self.length.get()))

    def generate(self):
        chars = string.ascii_lowercase
        if self.use_upper.get():
            chars += string.ascii_uppercase
        if self.use_digits.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += "!@#$%^&*()-_=+?"
        rng = random.SystemRandom()
        self.password.set("".join(rng.choice(chars) for _ in range(self.length.get())))
        self.status.set("")

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.password.get())
        self.status.set("Пароль скопійовано в буфер обміну ✔")


# ---------------------------------------------------------------- Конвертер одиниць
UNITS = {
    "Довжина": {"мм": 0.001, "см": 0.01, "м": 1, "км": 1000,
                "дюйм": 0.0254, "фут": 0.3048, "миля": 1609.344},
    "Вага": {"г": 0.001, "кг": 1, "т": 1000, "фунт": 0.45359237, "унція": 0.0283495},
    "Температура": {"°C": None, "°F": None, "K": None},
}


def convert_temperature(value, src, dst):
    celsius = {"°C": value, "°F": (value - 32) * 5 / 9, "K": value - 273.15}[src]
    return {"°C": celsius, "°F": celsius * 9 / 5 + 32, "K": celsius + 273.15}[dst]


class ConverterTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        self.category = tk.StringVar(value="Довжина")
        self.value = tk.StringVar(value="1")
        self.src = tk.StringVar()
        self.dst = tk.StringVar()
        self.result = tk.StringVar()

        ttk.Label(self, text="Конвертер одиниць", style="Title.TLabel").pack(anchor="w")

        cat = ttk.Combobox(self, textvariable=self.category, values=list(UNITS), state="readonly")
        cat.pack(fill="x", pady=(15, 10))
        cat.bind("<<ComboboxSelected>>", lambda e: self._fill_units())

        ttk.Entry(self, textvariable=self.value, font=("Segoe UI", 12)).pack(fill="x", ipady=3)

        row = ttk.Frame(self)
        row.pack(fill="x", pady=10)
        self.src_box = ttk.Combobox(row, textvariable=self.src, state="readonly", width=10)
        self.src_box.pack(side="left", expand=True, fill="x")
        ttk.Button(row, text="⇄", width=3, command=self.swap).pack(side="left", padx=8)
        self.dst_box = ttk.Combobox(row, textvariable=self.dst, state="readonly", width=10)
        self.dst_box.pack(side="left", expand=True, fill="x")

        ttk.Label(self, textvariable=self.result, style="Result.TLabel").pack(pady=15)

        for var in (self.value, self.src, self.dst):
            var.trace_add("write", lambda *a: self.convert())

        self._fill_units()

    def _fill_units(self):
        units = list(UNITS[self.category.get()])
        self.src_box["values"] = units
        self.dst_box["values"] = units
        self.src.set(units[0])
        self.dst.set(units[1])

    def swap(self):
        a, b = self.src.get(), self.dst.get()
        self.src.set(b)
        self.dst.set(a)

    def convert(self):
        try:
            value = float(self.value.get().replace(",", "."))
        except ValueError:
            self.result.set("Введіть число")
            return
        src, dst = self.src.get(), self.dst.get()
        table = UNITS[self.category.get()]
        # під час зміни категорії одна з одиниць ще може бути зі старого списку
        if src not in table or dst not in table:
            return
        if self.category.get() == "Температура":
            res = convert_temperature(value, src, dst)
        else:
            res = value * table[src] / table[dst]
        self.result.set(f"{value:g} {src} = {res:.4g} {dst}")


# ---------------------------------------------------------------- Вгадай число
class GuessTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        self.guess = tk.StringVar()
        self.hint = tk.StringVar()
        self.info = tk.StringVar()
        self.best = None

        ttk.Label(self, text="Вгадай число", style="Title.TLabel").pack(anchor="w")
        ttk.Label(self, text="Я загадав число від 1 до 100. Спробуй вгадати!").pack(anchor="w", pady=(10, 15))

        entry = ttk.Entry(self, textvariable=self.guess, font=("Segoe UI", 14), justify="center")
        entry.pack(fill="x", ipady=4)
        entry.bind("<Return>", lambda e: self.check())

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", pady=10)
        ttk.Button(buttons, text="Перевірити", command=self.check).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(buttons, text="Нова гра", command=self.new_game).pack(side="left", expand=True, fill="x", padx=(5, 0))

        ttk.Label(self, textvariable=self.hint, style="Result.TLabel").pack(pady=10)
        ttk.Label(self, textvariable=self.info).pack()

        self.new_game()

    def new_game(self):
        self.secret = random.randint(1, 100)
        self.attempts = 0
        self.finished = False
        self.guess.set("")
        self.hint.set("Чекаю на твою відповідь...")
        self._update_info()

    def _update_info(self):
        best = self.best if self.best is not None else "—"
        self.info.set(f"Спроб: {self.attempts}    Рекорд: {best}")

    def check(self):
        if self.finished:
            return
        try:
            n = int(self.guess.get())
        except ValueError:
            self.hint.set("Введіть ціле число")
            return
        if not 1 <= n <= 100:
            self.hint.set("Число має бути від 1 до 100")
            return

        self.attempts += 1
        if n < self.secret:
            self.hint.set(f"{n} — замало ⬆ Більше!")
        elif n > self.secret:
            self.hint.set(f"{n} — забагато ⬇ Менше!")
        else:
            self.hint.set(f"🎉 Вгадав! Це {n}")
            self.finished = True
            if self.best is None or self.attempts < self.best:
                self.best = self.attempts
        self.guess.set("")
        self._update_info()


# ---------------------------------------------------------------- Головне вікно
def main():
    root = tk.Tk()
    root.title("PocketTools")
    root.geometry("420x400")
    root.resizable(False, False)

    style = ttk.Style()
    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
    style.configure("Result.TLabel", font=("Segoe UI", 13))

    tabs = ttk.Notebook(root)
    tabs.pack(fill="both", expand=True, padx=8, pady=8)
    tabs.add(PasswordTab(tabs), text="🔑 Паролі")
    tabs.add(ConverterTab(tabs), text="📏 Конвертер")
    tabs.add(GuessTab(tabs), text="🎲 Вгадай число")

    root.mainloop()


if __name__ == "__main__":
    main()
