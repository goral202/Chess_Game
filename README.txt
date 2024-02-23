Projekt relizuje zadanie z przedmiotu WNO.

Projekt uruchamiany jest za pomoca uruchomienia pliku main.py.
Wyswietlane jest okno glowne do ktorego zalaczone zostaly plansza jako Sceana, dwa zegary jako Widgety oraz pole tekstowe jako Linia teskstu.


Szachy realizuja polecenia:
1. Dziedziczenie po QGraphicsScene. (plansza szachow znajdujaca sie w pliku board.py)
2. Dziedziczenie po QGraphicsItem . ( klasy pionkow w folderze pawns)                   
3. Każda bierka jest klikalna i przeciagalna. Klikniecie, przeciagniecie i upuszczenie bierniki realizuje jej ruch. Klikniecie prawym przyciskiem myszy na dowolna bierke wyswietla menu pozwalajace zminiec kolor planszy.
4. Na ekranie w lewym gornym rogu znajduje sie pole tekstowe pozwalajace poruszanie pionkami za pomoca notacji szachowej.
Notacja szachowa w formie Nxy, gdzie N to rodzaj bierki w polskiej notacji szachowej ('K'-'King';'H'-'Queen';'S'-'Knight';'G'-'Bishop';'W'-'Rook';brak - 'Pawn'), x - kolumna, y - wiersz.
5. Grafiki sa importowane z pliku resources.qrc.
6. Przytrzymanie bierki powoduje podswielenie mozliwych ruchow.
7. Gra realizuje niektore reguły gry (gra turowa, zbijanie bierek, promocje pionka, sprawdzenie szacha)
8. Na ekranie sa dwa klikalne analogowe zegary odliczajace czas w dol od 5 minut. Klikniecie dowolnego zegara powoduje zatrzymanie kliknietego zegara. Zegary nie zostaly do tej pory polaczone z reszta gry.

Punktacja:
1. 1pkt
2. 1pkt
3. 3pkt
4. 2pkt
5. 1pkt
6. 2pkt
7. 1pkt
8. 1pkt/2pkt


uzyte biblioteki: PyQt5, resources, sys