import json
import datetime
import matplotlib.pyplot as plt
from plyer import notification


class Zadanie:
    def __init__(self, tytul, termin, status="niezrobione"):
        self.tytul = tytul
        self.termin = termin
        self.status = statusgi

    def to_dict(self):
        return {"tytul": self.tytul, "termin": self.termin, "status": self.status}


class TrackerNauki:
    def __init__(self, plik_bazy="zadania.json"):
        self.plik_bazy = plik_bazy
        self.zaladuj_zadania()

    def zaladuj_zadania(self):
        try:
            with open(self.plik_bazy, "r") as plik:
                dane = json.load(plik)
                self.zadania = [Zadanie(**zad) for zad in dane]
        except FileNotFoundError:
            self.zadania = []

    def zapisz_zadania(self):
        with open(self.plik_bazy, "w") as plik:
            json.dump([zad.to_dict() for zad in self.zadania], plik, indent=2)

    def dodaj_zadanie(self, tytul, termin):
        self.zadania.append(Zadanie(tytul, termin))
        self.zapisz_zadania()

    def edytuj_zadanie(self, indeks, nowy_tytul=None, nowy_termin=None, nowy_status=None):
        zad = self.zadania[indeks]
        if nowy_tytul:
            zad.tytul = nowy_tytul
        if nowy_termin:
            zad.termin = nowy_termin
        if nowy_status:
            zad.status = nowy_status
        self.zapisz_zadania()

    def usun_zadanie(self, indeks):
        self.zadania.pop(indeks)
        self.zapisz_zadania()

    def przypomnienia(self):
        dzisiaj = datetime.date.today().isoformat()
        for zad in self.zadania:
            if zad.termin == dzisiaj and zad.status == "niezrobione":
                notification.notify(title="Przypomnienie o zadaniu",
                                    message=f"{zad.tytul} (do dzisiaj)", timeout=10)

    def pokaz_postep(self):
        zrobione = sum(1 for z in self.zadania if z.status == "zrobione")
        calkowite = len(self.zadania)
        if calkowite == 0:
            print("Brak zadań do pokazania postępu.")
            return
        procent = (zrobione / calkowite) * 100
        print(f"Postęp: {procent:.2f}%")

    def generuj_statystyki(self):
        daty = {}
        for zad in self.zadania:
            if zad.status == "zrobione":
                daty[zad.termin] = daty.get(zad.termin, 0) + 1

        if not daty:
            print("Brak danych do wygenerowania statystyk.")
            return

        daty_posortowane = dict(sorted(daty.items()))
        plt.bar(daty_posortowane.keys(), daty_posortowane.values())
        plt.title("Statystyki ukończonych zadań")
        plt.xlabel("Data")
        plt.ylabel("Liczba zadań")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    tracker = TrackerNauki()
    tracker.przypomnienia()

