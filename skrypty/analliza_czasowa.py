import pandas as pd
import numpy as np
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

df = pd.read_csv(CSV)

# znowu obróbka
df["TERYTC"] = df["TERYTC"].astype(str).str.zfill(4)
df = df[df["TERYTC"].isin(MIASTA_WOJ.keys())]
df["MIASTO"] = df["TERYTC"].map(MIASTA_WOJ)


trend = df.groupby(["ROK", "MIASTO"])["LICZBA"].sum().unstack(fill_value=0)

rok_list = trend.index.tolist()
miasta_list = trend.columns.tolist()
bar_width = 0.8 / len(miasta_list) 
x = np.arange(len(rok_list))

plt.figure(figsize=(16,8))
colors = plt.get_cmap("tab20").colors  

for i, miasto in enumerate(miasta_list):
    plt.bar(x + i*bar_width, trend[miasto], width=bar_width, label=miasto, color=colors[i % len(colors)])
    for xi, yi in zip(x + i*bar_width, trend[miasto]):
        plt.text(xi, yi, str(int(yi)), ha="center", va="bottom", fontsize=10, fontweight="bold")

plt.xlabel("Rok", fontsize=14, fontweight="bold")
plt.ylabel("Liczba obiektów rekreacyjnych", fontsize=14, fontweight="bold")
plt.title("Zmiany liczby obiektów rekreacyjnych w miastach wojewódzkich (2022–2024)",
          fontsize=16, fontweight="bold")
plt.xticks(x + bar_width*len(miasta_list)/2, rok_list, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.legend(title="Miasto", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=11, title_fontsize=12)
plt.tight_layout()
plt.show()