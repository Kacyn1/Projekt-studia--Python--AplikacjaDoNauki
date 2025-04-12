import tkinter as tk
from tkinter import messagebox, ttk
from main import TrackerNauki

class AplikacjaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tracker Nauki")
        self.tracker = TrackerNauki()

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.frame_zadania = ttk.Frame(notebook)
        notebook.add(self.frame_zadania, text="Zadania")

        self.frame_historia = ttk.Frame(notebook)
        notebook.add(self.frame_historia, text="Historia")

        self.lista = tk.Listbox(self.frame_zadania, width=50)  # Lista zadań
        self.lista.pack(pady=10)

        self.canvas = tk.Canvas(self.frame_zadania, width=300, height=30, bg="lightgray", highlightthickness=0)  # Pasek postępu na Canvas
        self.canvas.pack(pady=10)

        self.tytul_var = tk.StringVar()  # Pola do wpisywania zadania
        self.termin_var = tk.StringVar()

        tk.Label(self.frame_zadania, text="Tytuł zadania:").pack()
        tk.Entry(self.frame_zadania, textvariable=self.tytul_var).pack()
        tk.Label(self.frame_zadania, text="Termin (YYYY-MM-DD):").pack()
        tk.Entry(self.frame_zadania, textvariable=self.termin_var).pack()

        tk.Button(self.frame_zadania, text="Dodaj zadanie", command=self.dodaj_zadanie).pack(pady=5)  # Przyciski
        self.button_edytuj = tk.Button(self.frame_zadania, text="Edytuj zadanie", command=self.edytuj_zadanie)
        self.button_edytuj.pack(pady=5)
        tk.Button(self.frame_zadania, text="Usuń zaznaczone", command=self.usun_zadanie).pack(pady=5)
        tk.Button(self.frame_zadania, text="Oznacz jako zrobione", command=self.oznacz_jako_zrobione).pack(pady=5)

        self.lista_historia = tk.Listbox(self.frame_historia, width=50)  # Lista historii
        self.lista_historia.pack(pady=10)

        self.odswiez_liste()  # Załaduj początkową listę

    def odswiez_liste(self):
        self.lista.delete(0, tk.END)
        for i, zad in enumerate(self.tracker.zadania):
            status = "✓" if zad.status == "zrobione" else "✗"
            self.lista.insert(tk.END, f"{i+1}. {zad.tytul} [{status}] - {zad.termin}")
        self.aktualizuj_postep()
        self.odswiez_historie()

    def odswiez_historie(self):
        self.lista_historia.delete(0, tk.END)
        wykonane = [z for z in self.tracker.zadania if z.status == "zrobione"]
        for i, zad in enumerate(wykonane):
            self.lista_historia.insert(tk.END, f"{i+1}. {zad.tytul} - {zad.termin}")

    def dodaj_zadanie(self):
        tytul = self.tytul_var.get()
        termin = self.termin_var.get()
        if not tytul or not termin:
            messagebox.showwarning("Błąd", "Uzupełnij oba pola")
            return
        self.tracker.dodaj_zadanie(tytul, termin)
        self.tytul_var.set("")
        self.termin_var.set("")
        self.odswiez_liste()

    def usun_zadanie(self):
        zaznaczone = self.lista.curselection()
        if not zaznaczone:
            return
        self.tracker.usun_zadanie(zaznaczone[0])
        self.odswiez_liste()

    def oznacz_jako_zrobione(self):
        zaznaczone = self.lista.curselection()
        if not zaznaczone:
            return
        indeks = zaznaczone[0]
        self.tracker.edytuj_zadanie(indeks, nowy_status="zrobione")
        self.odswiez_liste()

    def aktualizuj_postep(self):
        self.canvas.delete("all")
        zrobione = sum(1 for z in self.tracker.zadania if z.status == "zrobione")
        calkowite = len(self.tracker.zadania)

        if calkowite == 0:
            procent = 0
        else:
            procent = (zrobione / calkowite) * 100

        szerokosc = int(3 * procent)  # 300px = 100%
        self.canvas.create_rectangle(0, 0, szerokosc, 30, fill="green", width=0)
        self.canvas.create_text(150, 15, text=f"Postęp: {procent:.2f}%", fill="white", font=("Arial", 12, "bold"))

    def edytuj_zadanie(self):
        edycja_okno = tk.Toplevel(self.root)  # Tworzymy nowe okno
        edycja_okno.title("Edytuj zadanie")

        lista_zadan = [f"{zad.tytul} - {zad.termin}" for zad in self.tracker.zadania]  # Wybór zadania do edytowania
        lista_zadan_combobox = tk.StringVar(value=lista_zadan)

        lista = tk.Listbox(edycja_okno, listvariable=lista_zadan_combobox, height=5, selectmode=tk.SINGLE)
        lista.pack(pady=5)

        label_tytul = tk.Label(edycja_okno, text="Tytuł:")  # Pola do edycji tytułu i terminu
        label_tytul.pack(pady=2)
        entry_tytul = tk.Entry(edycja_okno)
        entry_tytul.pack(pady=2)

        label_termin = tk.Label(edycja_okno, text="Termin (YYYY-MM-DD):")
        label_termin.pack(pady=2)
        entry_termin = tk.Entry(edycja_okno)
        entry_termin.pack(pady=2)

        def zapisz_edytowane():
            selected_index = lista.curselection()  # Pobieranie wybranego zadania
            if not selected_index:
                return

            zadanie = self.tracker.zadania[selected_index[0]]
            zadanie.tytul = entry_tytul.get()
            zadanie.termin = entry_termin.get()

            self.tracker.zapisz_zadania()  # Zapisz zmiany
            edycja_okno.destroy()
            self.odswiez_liste()

        def ustaw_pola(event):
            selected_index = lista.curselection()
            if selected_index:
                zadanie = self.tracker.zadania[selected_index[0]]
                entry_tytul.delete(0, tk.END)
                entry_tytul.insert(0, zadanie.tytul)
                entry_termin.delete(0, tk.END)
                entry_termin.insert(0, zadanie.termin)

        lista.bind("<<ListboxSelect>>", ustaw_pola)  # Ustaw domyślne wartości po kliknięciu

        button_zapisz = tk.Button(edycja_okno, text="Zapisz", command=zapisz_edytowane)  # Przycisk do zapisania edytowanych danych
        button_zapisz.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikacjaGUI(root)
    root.mainloop()
