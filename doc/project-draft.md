# Programowanie Zespołowe, dr Przemysław Kubiak, grupa wt 18:55 - 20:35

## Skład grupy

  - Piotr Chlebowski, 254666
  - Kacper Szatan, 236478
  - Łukasz Tomczak, 256467
  - Daniel Zatoń, 256327

## Temat projektu

Szyfrowany komunikator desktopowy

## Funkcjonalności

**Jako użytkownik:**

  1. Możliwość logowania/rejestracji w celu posiadania przenoszalnej, zsynchronizowanej pomiędzy urządzeniami,
     spersonalizowanej przestrzeni użytkownika.
  2. Tworzenie listy kontaktów (dodawanie, modyfikowanie, usuwanie).
  3. Tworzenie czatu z użytkownikiem przez wyszukanie go w bazie użytkowników (nickname lub email).
  4. Tworzenie czatów prywatnych/tajnych. Nie przechowujących historii na serwerze (tylko na urządzeniach).
  5. Statusy klienta (dostępny, zajety, zaraz wracam, itd.).
  6. Tworzenie czatów grupowych dodawanie usuwanie członków.
  7. Usuwanie konta z aplikacji.
  8. Blokowanie użytkowników (blacklista w której są wyszczególnione konta, które nie mogą do nas
     (jako użytkownika) pisać).
  9. Możliwość eksportowania i importowania na nowym urządzeniu, czatu/listy kontaktów.
 10. Wiadomości oraz czas ich wysałania są szyfrowane i niemożliwe do otczytania ze strony serwera.
 11. Wysyłanie, edytowanie i usuwanie własnych wiadomości.
     (oraz odpowiedzi i reakcje na nie).
 12. Powiadomienia z aplikacji (gdy użytkownik skupia uwage na czymś innym
     wciąż otrzyma notyfikację po otrzymaniu wiadomości).
 13. Wysyłanie wiadomości z ustawionym czasem usunięcia.
 14. Personalizacja szaty graficznej czatów i całej aplikacji (zmiana palety kolorów).
	
**Jako administrator:**

  1. Filtrowanie wiadomości.
  2. Banowanie użytkowników.
  3. Kompresja przechowywanych danych.

**Skalowalność:**

  1. Kompatybilnośc między wersjami komunikatora.
  2. Modularna budowa komponentów systemu.

## Scenariusze

**Rejestracja:**

- użytkownik ściąga aplikację kliencką
- użytkownik klika przycisk "Rejestruj"
- aplikacja prosi o nazwę użytkownika i hasło
- użytkownik wybiera czy chce aby aplikacja automatycznie
  wygenerowała klucze do komunikacji albo wskazuje je własnoręcznie
- klient przesyła zaszyfrowaną kluczem publicznym serwera wiadomość zawierającą:

   - nazwę użytkownika
   - klucz publiczny przypisany do konta
   - hash hasła
   - klucz prywatny zamaskowany innym hashem hasła
   - adres urządzenia

- serwer sprawdza dostępność loginu, jeśli tak to tworzy rekord dla użytkownika i potwierdza założenie konta
- użytkownik jest zalogowany

**Logowanie się:**

- użytkownik podaje login i hasło w aplikacji
- aplikacja przesyła serwerowi zaszyfrowaną jego kluczem publicznym wiadomość:

   - login
   - hash hasła

- serwer porównuje wartości z tymi zapisanymi w wewnętrznej bazie danych
- przesyłana jest wiadomość odmowna lub potwierdzająca, następuje synchronizacja
  lokalnej historii wiadomości
- serwer zapamiętuje urządzenie jako aktywne

**Logowanie przy braku kluczy (np. na nowym urządzeniu):**

- aplikacja generuje parę kluczy tymczasowych (potrzebne do zaszyfrowania wiadomości zwrotnej)
- do zaszyfrowanej wiadomości przesyłanej serwerowi dodatkowo załączone są:

   - prośba o oryginalny klucz publiczny
   - prośba o zaszyfrowany hasłem oryginalny klucz prywatny
   - tymczasowy klucz publiczny

- w razie poprawnej weryfikacji serwer załącza dodatkowo do wiadomości zwrotnej niezbędne dane,
  a samą wiadomość szyfruje otrzymanym kluczem tymczasowym
- aplikacja zastępuje klucze tymczasowe oryginałami

**Zakładanie czatu:**

- zalogowany użytkownik wyszukuje w aplikacji kontaktu
- użytkownik wybiera osobę z listy pasujących wyników
- otwiera się okno z możliwością wysyłania wiadomości
- czat zostaje przypięty w historii po otrzymaniu/wysłaniu pierwszej wiadomości

**Wysyłanie wiadomości:**

- aplikacja sprawdza obecność klucza publicznego odbiorcy na urządzeniu
- w razie braku klucza użytkownik wybiera z 2 możliwości:

  - automatyczne zaciągnięcie klucza z serwera
  - ręczne wprowadzenie klucza / pliku z kluczem

- użytkownik wybiera czy wiadomość ma być _tajna_ (niezapamiętywana przez serwer)
- aplikacja szyfruje treść wiadomości, datę i nadawcę kluczem publicznym odbiorcy, a następnie
  załącza identyfikator odbiorcy, szyfruje całość kluczem publicznym serwera i wysyła
- serwer odszyfrowywuje wiadomość i przesyła odbiorcy dalej zaszyfrowaną część

  - wiadomość tajna przesyłana jest na wszystkie obecnie aktywne urządzenia odbiorcy
    lub na pierwsze które się pojawi, a następnie jest usuwana z serwera
  - wiadomości nietajne zostają zapisane na serwerze

- odbiorca odszyfrowywuje odebrane wiadomości i przechowywuje lokalnie (zaszyfrowane)

**Eksport historii:**

- użytkownik wybiera opcję eksportu lokalnej historii i zcache'owanych kluczy publicznych kontaktów
- aplikacja pyta użytkownika o hasło jakim będzie zaszyfrowany plik
- historia i klucze publiczne innych użykowników są odkodowywane hashem głównego hasła i zaszyfrowywane
   hashem nowowprowadzonego

**Import historii:**

- użytkownik wybiera opcję importu do historii z pliku
- aplikacja prosi o wskazanie pliku oraz podanie odpowiedniego hasła
- historia i klucze publiczne innych użykowników są importowane do lokalnej historii

**Zmiana kluczy do komunikacji:**

- użytkownik wybiera opcję zmiany klucza w aplikacji
- użytkownik wybiera czy chce aby aplikacja automatycznie
  wygenerowała klucze do komunikacji albo wskazuje je własnoręcznie
- aplikacja prosi o hasło i weryfikuje je
- klient przesyła zaszyfrowaną kluczem publicznym serwera wiadomość zawierającą:

   - klucz publiczny
   - zamaskowany klucz prywatny

- serwer nadpisuje dotychczasową parę i wysyła wiadomość zwrotną o sukcesie
- aplikacja klienta nadpisuje lokalnie klucze i wysyła serwerowi historię nietajnych wiadomości
   zaszyfrowanych nowym kluczem publicznym
- serwer powiadamia wszystkie inne zalogowane aplikacje użytkownika o zmianie kluczy
- aplikacje zaciągają nową parę kluczy
- wszyskie aplikacje klienckie użytkownika przesyłają znanym nadawcom nowy klucz publiczny

**Zmiana hasła:**

- użytkownik wybiera opcję zmiany hasła w aplikacji
- użytkownik wpisuje raz stare i dwukrotnie nowe hasło, sprawdzana jest ich zgodność
- aplikacja przesyła serwerowi zaszyfrowaną jego kluczem publicznym wiadomość zawierającą

  - hash starego hasła
  - hash nowego hasła
  - klucz prywatny do komunikacji zamaskowany innym hashem nowego hasła

- przy zgodności starego hasha serwer wysyła urządzeniu informację zwrotną o sukcesie
- lokalna baza danych jest odkodowywana starym i zaszyfrowywana nowy hasłem
- serwer wysyła równocześnie wszystkim innym aktywnym urządzeniom użytkownika
  informację o zmianie hasła
- każde z nich zaciąga z serwera nową parę hash + zamaskowany klucz prywatny
- na podstawie loklalnie przechowywanego klucza prywatnego i jego nowozamaskowanej wersji
  uzyskiwany jest drugi hash nowego hasła
- lokalna baza danych jest odpowiednia przekodowywana
- aplikacja wylogowywuje się / prosi o nowe hasło w celu kontynuacji

## Używane technologie

**Języki programowania, frameworki:**

  - Python
  - pyQt/pyGTK/wxPython
  - SQL (backend)

**Zarządzanie kodem, podział zadań:**

  - git + Github

## Parametry

**Platforma:**

GNU/Linux

**Ewentualne możliwości rozszerzenia projektu:**

  1. Stworzenie kompatybilnej wersji na systemy Windows/MacOS.
  2. Możliwość utworzenia czatu głosowego, czatów wideo.
  3. Interpretacja syntaksu markdown w wiadomościach.
  4. Możliwość utworzenia serwerów lokalnych tworzonych przez klientów za pomocą aplikacji serwera.
  5. System dystrybucji komunkatora:
     Strona internetowa z przyciskiem "download client/server"
  6. Menadżer aktualizacji/instalacji komunikatora.
