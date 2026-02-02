import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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

df = pd.read_csv(CSV)
df["TERYTC"] = df["TERYTC"].astype(str).str.zfill(4)
df = df[df["TERYTC"].isin(MIASTA_WOJ.keys())]
df["MIASTO"] = df["TERYTC"].map(MIASTA_WOJ)
df["RODZAJ"] = df["RODZAJ"].fillna("inne")
df["RODZAJ"] = df["RODZAJ"].apply(lambda x: str(x).strip() if str(x).strip() else "inne")

#grupowanie miasto, rodzaj, listowanie i gradient
pivot = df.groupby(["MIASTO", "RODZAJ"])["LICZBA"].sum().reset_index()
miasta = pivot["MIASTO"].unique()
def fiolet_gradient(n):
    cmap = plt.get_cmap("Purples")
    return [cmap(0.3 + 0.7*i/(n-1)) for i in range(n)]

def rysuj_pie(miasto, threshold_percent=2):
    df_m = pivot[pivot["MIASTO"] == miasto].copy()
    total = df_m["LICZBA"].sum()
    
    # Małe wartości grupujemy do "inne"- straszny syf sie robił jak było 10 wartości 0.2 nałożonych na siebie graficznie
    df_m["PROCENT"] = df_m["LICZBA"] / total * 100
    df_small = df_m[df_m["PROCENT"] < threshold_percent]
    df_large = df_m[df_m["PROCENT"] >= threshold_percent]
    
    if not df_small.empty:
        inne_row = pd.DataFrame({
            "MIASTO":[miasto],
            "RODZAJ":["inne"],
            "LICZBA":[df_small["LICZBA"].sum()],
            "PROCENT":[df_small["PROCENT"].sum()]
        })
        df_plot = pd.concat([df_large, inne_row], ignore_index=True)
    else:
        df_plot = df_large

    df_plot = df_plot.sort_values("LICZBA", ascending=False).reset_index(drop=True)
    
    labels = df_plot["RODZAJ"]
    values = df_plot["LICZBA"]
    
    colors = fiolet_gradient(len(labels))
    
    fig, ax = plt.subplots(figsize=(8,8))
    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,  
        autopct=lambda pct: f"{pct:.1f}%", 
        startangle=90,
        colors=colors,
        wedgeprops={'edgecolor':'white', 'linewidth':1}
    )
    
    # Legenda 
    legend_labels = [f"{lbl} ({val})" for lbl, val in zip(labels, values)]
    ax.legend(
        wedges,
        legend_labels,
        title="Typ / Liczba",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.3, 1),
        fontsize=10,
        title_fontsize=12,
        frameon=True,
        facecolor="white",
        framealpha=0.9
    )
    
    ax.set_title(f"Struktura typów obiektów rekreacyjnych w {miasto}", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

while True:
    print("\nMiasta wojewódzkie:")
    for i, m in enumerate(miasta):
        print(f"{i+1}. {m}")
    wybor = input("Wybierz miasto (numer) lub wpisz 'q' aby zakończyć: ")
    
    if wybor.lower() == 'q':
        break
    try:
        idx = int(wybor) - 1
        if 0 <= idx < len(miasta):
            rysuj_pie(miasta[idx])
        else:
            print("Niepoprawny numer.")
    except:
        print("Wpisz numer lub 'q'.")