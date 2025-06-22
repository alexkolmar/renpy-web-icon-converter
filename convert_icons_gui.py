import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

def create_icons_gui(source_path, output_dir, maskable_scale):
    os.makedirs(output_dir, exist_ok=True)

    with Image.open(source_path).convert("RGBA") as original:
        for size in ICON_SIZES:
            # Обычная иконка
            resized = original.resize((size, size), Image.LANCZOS)
            resized.save(os.path.join(output_dir, f"icon-{size}x{size}.png"))

            # Maskable иконка
            inner = int(size * maskable_scale)
            icon = original.resize((inner, inner), Image.LANCZOS)
            canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            pos = ((size - inner) // 2, (size - inner) // 2)
            canvas.paste(icon, pos, icon)
            canvas.save(os.path.join(output_dir, f"icon-{size}x{size}-maskable.png"))

def run_gui():
    def select_input():
        path = filedialog.askopenfilename(
            filetypes=[("PNG Images", "*.png"), ("All files", "*.*")]
        )
        if path:
            input_entry.delete(0, tk.END)
            input_entry.insert(0, path)

    def select_output():
        path = filedialog.askdirectory()
        if path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, path)

    def convert():
        source = input_entry.get()
        output = output_entry.get()
        try:
            scale = float(scale_entry.get())
            if not (0 < scale < 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Масштаб должен быть числом от 0 до 1.")
            return

        if not source or not os.path.exists(source):
            messagebox.showerror("Ошибка", "Выберите исходный файл.")
            return
        if not output:
            messagebox.showerror("Ошибка", "Выберите папку для сохранения.")
            return

        try:
            create_icons_gui(source, output, scale)
            messagebox.showinfo("Готово", "Иконки успешно сгенерированы!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Что-то пошло не так:\n{e}")

    # --- Интерфейс ---
    root = tk.Tk()
    root.title("Icon Converter")

    tk.Label(root, text="Исходный файл PNG:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    input_entry = tk.Entry(root, width=50)
    input_entry.grid(row=0, column=1, padx=5)
    tk.Button(root, text="Обзор...", command=select_input).grid(row=0, column=2, padx=5)

    tk.Label(root, text="Папка для сохранения:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=1, column=1, padx=5)
    tk.Button(root, text="Обзор...", command=select_output).grid(row=1, column=2, padx=5)

    tk.Label(root, text="Масштаб (maskable):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    scale_entry = tk.Entry(root, width=10)
    scale_entry.insert(0, "0.6")
    scale_entry.grid(row=2, column=1, sticky="w", padx=5)

    ttk.Separator(root, orient="horizontal").grid(row=3, columnspan=3, sticky="ew", pady=10)
    tk.Button(root, text="Конвертировать!", command=convert, bg="#4CAF50", fg="white", padx=20, pady=5).grid(row=4, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
