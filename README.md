# Pitfall - Dokumentacja Projektu Zaliczeniowego

## Wstęp i Opis Gry
Projekt stanowi implementację klasycznej gry zręcznościowej typu platformowego, stworzoną w języku Python przy użyciu biblioteki Pygame. Głównym celem rozgrywki jest przetrwanie jak najdłuższego czasu poprzez unikanie dynamicznie generowanych przeszkód oraz zdobywanie kolejnych poziomów trudności. Aplikacja została zaprojektowana z naciskiem na czystość kodu, obiektowość oraz skalowalność, realizując wymagania projektowe na ocenę bardzo dobrą.

## Architektura i Wzorce Projektowe
Rdzeń logiki aplikacji opiera się na **Wzorcu Maszyny Stanów (State Machine)**. Wykorzystano biblioteczną klasę `Enum` do ścisłego zdefiniowania dostępnych stanów aplikacji, takich jak MENU, GAME oraz GAME_OVER. Takie podejście gwarantuje deterministyczny przepływ sterowania i ułatwia zarządzanie przejściami między ekranami. Kod źródłowy został podzielony na logiczne moduły, separując logikę gry (`game.py`) od definicji obiektów (`player.py`, `barrel.py`, `rope.py`).

## Programowanie Obiektowe i Dziedziczenie
W projekcie zastosowano zaawansowane mechanizmy obiektowe. Zaimplementowano własną hierarchię klas, której fundamentem jest klasa bazowa `Image`. Odpowiada ona za wspólne aspekty obiektów graficznych, takie jak ładowanie tekstur czy zarządzanie prostokątami kolizji. Klasy konkretne, w tym `Player` i `Barrel`, dziedziczą bezpośrednio po klasie `Image`, rozszerzając ją o unikalne mechaniki ruchu i animacji. Jest to kluczowy element realizujący wymóg dziedziczenia po własnej klasie.

## Jakość Kodu i Typowanie
Cały projekt został napisany zgodnie ze standardami nowoczesnego Pythona. Zastosowano pełne typowanie statyczne (Type Hinting) dla wszystkich funkcji i metod. Definicje takie jak `def update(self, dt: float) -> None` zwiększają czytelność kodu, ułatwiają pracę środowiskom programistycznym i minimalizują ryzyko błędów typów w trakcie działania programu.

## System Zapisu i Obsługa Plików
Gra posiada trwały system zapisu postępów (Persistence). Po zakończeniu każdej rozgrywki moduł `game.py` otwiera plik `wyniki.txt` w trybie dopisywania i archiwizuje uzyskany wynik wraz z aktualną datą i osiągniętym poziomem. Mechanizm ten spełnia wymaganie dotyczące operacji na plikach oraz przetwarzania danych tekstowych.

## Mechanika i Proceduralne Generowanie
Poziom trudności nie jest statyczny, lecz generowany proceduralnie. Metoda `setup_level` dynamicznie dobiera zestawy przeszkód oraz skaluje prędkość poruszania się przeciwników w zależności od postępów gracza. Zastosowano również prostą sztuczną inteligencję dla obiektów typu `Barrel`, które samodzielnie zarządzają swoim cyklem życia i resetują swoją pozycję po opuszczeniu widocznego obszaru gry.

## Instrukcja Instalacji i Uruchomienia
Wymagane jest posiadanie zainstalowanego interpretera Python oraz biblioteki Pygame. Instrukcje uruchomienia:

`pip install pygame`

Uruchomienie gry następuje poprzez wywołanie głównego skryptu:

`python main.py`

## Sterowanie
Interakcja z grą odbywa się za pomocą klawiatury i myszy. Klawisze **Strzałek** lub **WSAD** służą do poruszania postacią. Klawisz **Spacja** odpowiada za skok oraz restart gry po porażce. Interakcja menu głownego odbywa się za pomocą myszki
