Analiza dostępności obiektów rekreacyjnych w miastach wojewódzkich w latach 2022–2024

Celem projektu jest analiza zmian w dostępności obiektów rekreacyjnych w miastach wojewódzkich w Polsce w latach 2022–2024, przeprowadzona na podstawie danych przestrzennych BDOT10k. Projekt koncentruje się na ilościowym i przestrzennym ujęciu dostępności.

Cel projektu : 

- identyfikacja i selekcja obiektów rekreacyjnych na podstawie danych BDOT10k,
- określenie liczby obiektów rekreacyjnych w poszczególnych miastach wojewódzkich,
- analiza zmian liczby obiektów w ujęciu czasowym (2022–2024),
- analiza struktury obiektów rekreacyjnych według pola RODZAJ,
- przygotowanie danych wynikowych do dalszej wizualizacji i interpretacji.

Wykorzystane narzędzia : 

- Visual Studio Code - język Python 
- ArcGIS Pro

Dane użyte do projektu : 

- Bazy Danych Obiektów Topograficznych BDOT10k

Opis i zastosowanie skryptów :

-> Skrypt 1 - Pobierz dane 

Celem tego skryptu jest pobranie danych z Archiwum Bazy Danych Obiektów Topograficznych (BDOT10k) udostępnionego na Geoportalu. Skrypt pobiera warstwy  BUSP oraz KUSK dla lat 2022–2024, natomiast warstwa granic administracyjnych ADMS pobierana jest wyłącznie dla roku 2024 i wykorzystywana jako warstwa referencyjna w dalszych analizach.
W trakcie działania skrypt tworzy geobazę, w której zapisywane są warstwy wynikowe, oraz dodaje pole atrybutowe ROK, wykorzystywane w kolejnych skryptach analitycznych.

-> Skrypt 2 - Przygotuj dane

Celem tego skryptu jest przeprowadzenie analizy przestrzennej obiektów rekreacyjnych oraz przypisanie ich do miast wojewódzkich na podstawie granic administracyjnych. Skrypt analizuje obiekty według pola atrybutowego RODZAJ, przy czym w przypadku braku wartości w tym polu obiekty klasyfikowane są do kategorii „inne”. 
Wyniki analizy są następnie agregowane i zapisywane w postaci tabelarycznej (CSV), stanowiącej podstawę do dalszych analiz statystycznych i wizualizacji.

-> Skrypt 3 - Porównanie misat wojewódzkich 

Celem tego skryptu jest wczytanie wyników analizy dostępności obiektów rekreacyjnych zapisanych w pliku CSV, agregacja danych dla miast wojewódzkich oraz  utworzenie rankingu miast według łącznej liczby obiektów rekreacyjnych w latach 2022–2024. Po uruchomieniu skryptu dane przedstawiane są w postaci wykresu słupkowego.

-> Skrypt 4 - Analiza czasowa 

Celem tego skryptu jest analiza zmian liczby obiektów rekreacyjnych w miastach wojewódzkich w ujęciu czasowym, porównanie dynamiki zmian pomiędzy miastami i przedstawienie jej w formie graficznej przy użyciu wykresu.
Skrypt pozwala odpowiedzieć na pytanie, czy w danym okresie nastąpił wzrost, spadek lub stabilizacja dostępności infrastruktury rekreacyjnej.

-> Skrypt 5 - Analiza struktury rodzaju 

Celem tego skryptu jest analiza struktury obiektów rekreacyjnych według pola RODZAJ, porównanie udziału poszczególnych typów obiektów w miastach wojewódzkich, wizualizacja struktury danych w postaci wykresów kołowych.
