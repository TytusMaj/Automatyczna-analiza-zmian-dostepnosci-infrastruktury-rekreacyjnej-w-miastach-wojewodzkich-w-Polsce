import arcpy
import os
import requests
import zipfile
import shutil

# ==========================================================
# KONFIGURACJA
# ==========================================================
TEMP_DIR = r"D:\T"
GEOBAZA  = r"D:\ProjektPPA_dane\ProjektPPA\ProjektPPA.gdb"
BASE_URL = "https://opendata.geoportal.gov.pl/Archiwum/bdot10k"
LATA = [2022, 2023, 2024]

# Rok, z którego chcemy pobrać granice (ADMS). Dla innych lat granice zostaną pominięte.
ROK_TYLKO_DLA_GRANIC = 2024 

WARSTWY = ["BUBD", "ADMS", "KUSK", "BUSP", "SKRP", "SKJZ"]

MIASTA = {
    "02": ["0264"], "04": ["0461", "0463"], "06": ["0661"],
    "08": ["0861", "0862"], "10": ["1061"], "12": ["1261"],
    "14": ["1465"], "16": ["1661"], "18": ["1861"],
    "20": ["2061"], "22": ["2261"], "24": ["2469"],
    "26": ["2661"], "28": ["2861"], "30": ["3064"], "32": ["3262"]
}

# ==========================================================
# INICJALIZACJA (Tworzenie GDB)
# ==========================================================
print("=== INICJALIZACJA ===")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

folder_projektu = os.path.dirname(GEOBAZA)
if not os.path.exists(folder_projektu):
    os.makedirs(folder_projektu)

if not arcpy.Exists(GEOBAZA):
    print(f"[INIT] Tworzę geobazę: {GEOBAZA}")
    try:
        arcpy.management.CreateFileGDB(folder_projektu, os.path.basename(GEOBAZA))
    except Exception as e:
        print(f"[!!!] BŁĄD GDB: {e}")
        exit()

arcpy.env.workspace = GEOBAZA
arcpy.env.overwriteOutput = True

# ==========================================================
# FUNKCJE
# ==========================================================

def pobierz_i_rozpakuj(rok, woj, teryt):
    url = f"{BASE_URL}/{rok}/SHP/{woj}/{teryt}_SHP_{rok}.zip"
    zip_path = os.path.join(TEMP_DIR, "temp.zip")
    extract_path = os.path.join(TEMP_DIR, f"d_{teryt}")

    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
    os.makedirs(extract_path)

    print(f"\n[PROCES] TERYT: {teryt} | ROK: {rok}")
    try:
        r = requests.get(url, stream=True, timeout=60)
        if r.status_code == 200:
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(extract_path)
            
            if os.path.exists(zip_path): os.remove(zip_path)
            return extract_path
        else:
            print(f"  [!] Błąd HTTP: {r.status_code}")
            return None
    except Exception as e:
        print(f"  [!] Wyjątek sieciowy: {e}")
        return None

def importuj_dane(folder, rok, teryt):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".shp"):
                fn_lower = f.lower()
                
                for kod in WARSTWY:
                    kod_low = kod.lower()
                    if f"_{kod_low}_" in fn_lower or fn_lower.endswith(f"_{kod_low}.shp"):
                        
                        # --- FILTR GRANIC ---
                        # Jeśli to ADMS, a rok nie jest 2024 -> pomiń
                        if kod == "ADMS" and rok != ROK_TYLKO_DLA_GRANIC:
                            continue
                        # --------------------

                        try:
                            parts = fn_lower.replace(".shp", "").split("_")
                            typ = parts[-1] if parts else "x"
                            
                            nazwa_warstwy = f"{kod_low}_{typ}_{rok}_{teryt}"
                            sciezka_wyjsciowa = os.path.join(GEOBAZA, nazwa_warstwy)

                            if arcpy.Exists(sciezka_wyjsciowa):
                                print(f"  [.] Już jest: {nazwa_warstwy}")
                                continue

                            # Fix 000732 (zmiana nazwy pliku)
                            base_orig = f[:-4]
                            nowa_base = f"t_{kod_low}_{typ}"
                            path_shp_temp = os.path.join(root, nowa_base + ".shp")
                            
                            for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg", ".sbn", ".sbx", ".xml"]:
                                src = os.path.join(root, base_orig + ext)
                                dst = os.path.join(root, nowa_base + ext)
                                if os.path.exists(src):
                                    if os.path.exists(dst): os.remove(dst)
                                    os.rename(src, dst)

                            if os.path.exists(path_shp_temp):
                                arcpy.conversion.ExportFeatures(path_shp_temp, sciezka_wyjsciowa)
                                print(f"  [+] IMPORT OK: {nazwa_warstwy}")

                        except Exception as e:
                            if "000258" not in str(e):
                                print(f"  [!] Błąd: {e}")

# ==========================================================
# START
# ==========================================================

for rok in LATA:
    print(f"\n--- ROK {rok} ---")
    for woj, teryty in MIASTA.items():
        for teryt in teryty:
            folder_danych = pobierz_i_rozpakuj(rok, woj, teryt)
            if folder_danych:
                importuj_dane(folder_danych, rok, teryt)
                try:
                    shutil.rmtree(folder_danych)
                except:
                    pass

print("\n=== GOTOWE ===")