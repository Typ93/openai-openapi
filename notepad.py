import tkinter as tk
from tkinter import filedialog, messagebox


class Notatnik(tk.Tk):
    """Prosty notatnik z opcją pozostawania na wierzchu."""

    def __init__(self):
        super().__init__()
        self.title("Notatnik")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.text = tk.Text(self, wrap="word")
        self.text.pack(fill="both", expand=True)

        self.topmost_var = tk.BooleanVar(value=False)
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nowy", command=self.new_file)
        filemenu.add_command(label="Otwórz", command=self.open_file)
        filemenu.add_command(label="Zapisz", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Wyjście", command=self.on_exit)
        menubar.add_cascade(label="Plik", menu=filemenu)

        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_checkbutton(
            label="Zawsze na wierzchu",
            variable=self.topmost_var,
            command=self.toggle_topmost,
        )
        menubar.add_cascade(label="Widok", menu=viewmenu)

        self.config(menu=menubar)

    def new_file(self):
        if self.confirm_discard_changes():
            self.text.delete("1.0", tk.END)

    def open_file(self):
        if not self.confirm_discard_changes():
            return
        path = filedialog.askopenfilename(
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się otworzyć pliku:\n{e}")

    def save_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")],
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.text.get("1.0", tk.END))
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać pliku:\n{e}")

    def toggle_topmost(self):
        self.attributes("-topmost", self.topmost_var.get())

    def confirm_discard_changes(self):
        return messagebox.askokcancel(
            "Potwierdź",
            "Czy na pewno chcesz kontynuować? Niezapisane zmiany zostaną utracone.",
        )

    def on_exit(self):
        if self.confirm_discard_changes():
            self.destroy()


if __name__ == "__main__":
    app = Notatnik()
    app.mainloop()
