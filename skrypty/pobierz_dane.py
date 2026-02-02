import arcpy
import os
import requests
import zipfile
import shutil


TEMP_DIR = r"C:\Users\Tytus\Desktop\ppa_projekt\Dane\temp_bdot10k"
GEOBAZA  = r"C:\Users\Tytus\Desktop\ppa_projekt\Dane\Warstwy\ProjektPPA.gdb"
BASE_URL = "https://opendata.geoportal.gov.pl/Archiwum/bdot10k"
LATA = [2022, 2023, 2024]

ROK_TYLKO_DLA_GRANIC = 2024

WARSTWY = ["ADMS", "KUSK", "BUSP"]

MIASTA = {
    "02": ["0264"], "04": ["0461", "0463"], "06": ["0663"],
    "08": ["0861", "0862"], "10": ["1061"], "12": ["1261"],
    "14": ["1465"], "16": ["1661"], "18": ["1863"],
    "20": ["2061"], "22": ["2261"], "24": ["2469"],
    "26": ["2661"], "28": ["2862"], "30": ["3064"], "32": ["3262"]
}


print("=== ROZPOCZĘCIE PROCESU ===")

os.makedirs(TEMP_DIR, exist_ok=True)

folder_projektu = os.path.dirname(GEOBAZA)
os.makedirs(folder_projektu, exist_ok=True)

if not arcpy.Exists(GEOBAZA):
    print(f"[INIT] Tworzę geobazę: {GEOBAZA}")
    arcpy.management.CreateFileGDB(folder_projektu, os.path.basename(GEOBAZA))

arcpy.env.workspace = GEOBAZA
arcpy.env.overwriteOutput = True



def dodaj_rok(fc, rok):
    pola = [f.name.lower() for f in arcpy.ListFields(fc)]
    if "rok" not in pola:
        arcpy.management.AddField(fc, "rok", "SHORT")
    arcpy.management.CalculateField(fc, "rok", rok)


def pobierz_i_rozpakuj(rok, woj, teryt):
    url = f"{BASE_URL}/{rok}/SHP/{woj}/{teryt}_SHP_{rok}.zip"
    zip_path = os.path.join(TEMP_DIR, "temp.zip")
    extract_path = os.path.join(TEMP_DIR, f"d_{teryt}")

    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
    os.makedirs(extract_path)

    print(f"\n[PROCES] TERYT: {teryt} | ROK: {rok}")

    r = requests.get(url, stream=True, timeout=60)
    if r.status_code != 200:
        print(f"  [!] Błąd HTTP: {r.status_code}")
        return None

    with open(zip_path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_path)

    os.remove(zip_path)
    return extract_path


def importuj_dane(folder, rok, teryt):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if not f.lower().endswith(".shp"):
                continue

            fn_lower = f.lower()

            for kod in WARSTWY:
                kod_low = kod.lower()

                if f"_{kod_low}_" in fn_lower or fn_lower.endswith(f"_{kod_low}.shp"):

                    if kod == "ADMS" and rok != ROK_TYLKO_DLA_GRANIC:
                        continue
                    try:
                        parts = fn_lower.replace(".shp", "").split("_")
                        typ = parts[-1] if parts else "x"

                        nazwa_warstwy = f"{kod_low}_{typ}_{rok}_{teryt}"
                        sciezka_wyjsciowa = os.path.join(GEOBAZA, nazwa_warstwy)

                        if arcpy.Exists(sciezka_wyjsciowa):
                            print(f"  [.] Już jest: {nazwa_warstwy}")
                            continue

                        # Bład 000732 - zbyt długa nazwa/ złe znaki 
                        base_orig = f[:-4]
                        nowa_base = f"t_{kod_low}_{typ}"
                        path_shp_temp = os.path.join(root, nowa_base + ".shp")

                        for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg", ".sbn", ".sbx", ".xml"]:
                            src = os.path.join(root, base_orig + ext)
                            dst = os.path.join(root, nowa_base + ext)
                            if os.path.exists(src):
                                if os.path.exists(dst):
                                    os.remove(dst)
                                os.rename(src, dst)

                        if os.path.exists(path_shp_temp):
                            arcpy.conversion.ExportFeatures(path_shp_temp, sciezka_wyjsciowa)
                            dodaj_rok(sciezka_wyjsciowa, rok)
                            print(f"  [+] IMPORT OK: {nazwa_warstwy}")

                    except Exception as e:
                        if "000258" not in str(e):
                            print(f"  [!] Błąd: {e}")



for rok in LATA:
    print(f"\n--- ROK {rok} ---")
    for woj, teryty in MIASTA.items():
        for teryt in teryty:
            folder_danych = pobierz_i_rozpakuj(rok, woj, teryt)
            if folder_danych:
                importuj_dane(folder_danych, rok, teryt)
                shutil.rmtree(folder_danych, ignore_errors=True)

print("\n=== GOTOWE ===")