import pandas as pd
import matplotlib.pyplot as plt

CSV = r"C:\Users\Tytus\Desktop\ppa_projekt\Dane\Dostepnosc_rekreacja_2022_2024.csv"


MIASTA_WOJ = {
    "0264": "Wrocław",
    "0461": "Bydgoszcz",
    "0463": "Toruń",
    "0663": "Lublin",
    "0861": "Gorzów Wlkp.",
    "0862": "Zielona góra",   
    "1061": "Łódź",
    "1261": "Kraków",
    "1465": "Warszawa",
    "1661": "Opole",
    "1863": "Rzeszów",
    "2061": "Białystok",
    "2261": "Gdańsk",
    "2469": "Katowice",
    "2661": "Kielce",
    "2862": "Olsztyn",
    "3064": "Poznań",
    "3262": "Szczecin"
}

# read i obróbka danych do reprezentacji
df = pd.read_csv(CSV)
df["TERYTC"] = df["TERYTC"].astype(str).str.zfill(4)
df = df[df["TERYTC"].isin(MIASTA_WOJ.keys())]
df["MIASTO"] = df["TERYTC"].map(MIASTA_WOJ)

#suma w rankingu
ranking = df.groupby("MIASTO")["LICZBA"].sum().sort_values(ascending=False)
print(ranking)

# rysowanie wykresu
if not ranking.empty:
    plt.figure(figsize=(12,6))
    ax = ranking.plot(kind="bar", color="skyblue")
    plt.xlabel("Miasto wojewódzkie")
    plt.ylabel("Liczba obiektów rekreacyjnych")
    plt.title("Ranking miast wojewódzkich – dostępność rekreacji (2022–2024)")
    plt.xticks(rotation=45, ha="right")
    
    for p in ax.patches:
        ax.annotate(str(int(p.get_height())),
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha="center", va="bottom", fontsize=10, color="black")
    
    plt.tight_layout()
    plt.show()
else:
    print("[!] Brak danych do narysowania wykresu")