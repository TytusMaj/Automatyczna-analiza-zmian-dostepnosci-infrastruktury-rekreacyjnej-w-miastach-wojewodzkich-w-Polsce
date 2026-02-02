import arcpy
import csv
import os
from collections import Counter

arcpy.env.workspace = r"C:\Users\Tytus\Desktop\ppa_projekt\Dane\Warstwy\ProjektPPA.gdb"
arcpy.env.overwriteOutput = True

MIASTA_WOJ = [
    "0264","0461","0463","0663","0861","0862","1061","1261",
    "1465","1661","1863","2061","2261","2469","2661","2862",
    "3064","3262"
]

OUT_FOLDER = r"C:\Users\Tytus\Desktop\ppa_projekt\Dane"
OUT_CSV = os.path.join(
    OUT_FOLDER,
    "Dostepnosc_rekreacja_2022_2024.csv"
)

adms_list = arcpy.ListFeatureClasses("adms*2024*")
if not adms_list:
    raise Exception("Brak warstwy ADMS z 2024 roku")

granice_miast = adms_list[0]
print(f"Granice miast: {granice_miast}")

busp = arcpy.ListFeatureClasses("busp*")
kusk = arcpy.ListFeatureClasses("kusk*")

warstwy = busp + kusk
print(f"BUSP: {len(busp)} | KUSK: {len(kusk)}")

wyniki = []

for warstwa in warstwy:

    print(f"\n[ANALIZA] {warstwa}")

    pola = [f.name.upper() for f in arcpy.ListFields(warstwa)]
    if "RODZAJ" not in pola:
        print("  [!] Brak pola RODZAJ – pominięto")
        continue

    arcpy.management.MakeFeatureLayer(warstwa, "tmp_lyr")

    sj = f"sj_{warstwa}"
    arcpy.analysis.SpatialJoin(
        target_features="tmp_lyr",
        join_features=granice_miast,
        out_feature_class=sj,
        join_operation="JOIN_ONE_TO_ONE",
        match_option="INTERSECT"
    )

    with arcpy.da.SearchCursor(sj, ["TERYT", "ROK", "RODZAJ"]) as cursor:
        for teryt, rok, rodzaj in cursor:

            if teryt not in MIASTA_WOJ:
                continue

            if rodzaj is None or str(rodzaj).strip() == "":
                rodzaj = "inne"

            wyniki.append((teryt, rok, rodzaj))

    arcpy.management.Delete("tmp_lyr")
    arcpy.management.Delete(sj)

counter = Counter(wyniki)

os.makedirs(OUT_FOLDER, exist_ok=True)

with open(OUT_CSV, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["TERYTC", "ROK", "RODZAJ", "LICZBA"])

    for (teryt, rok, rodzaj), liczba in sorted(counter.items()):
        writer.writerow([teryt, rok, rodzaj, liczba])

print("\n=== ANALIZA ZAKOŃCZONA POMYŚLNIE ===")
print(f"[OK] Plik CSV zapisany: {OUT_CSV}")
