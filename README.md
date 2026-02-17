# Analiza trendów w mediach społecznościowych z wykorzystaniem Redis

### Przedmiot: Bazy NoSQL
### Temat: 3.8 Analiza trendów w social media
### Autor: Oleksandra Basarab

1. Cel projektu

Celem projektu było zaprojektowanie i implementacja systemu do analizy trendów hashtagów w mediach społecznościowych z wykorzystaniem bazy danych NoSQL Redis.

System umożliwia:

- rejestrowanie zdarzeń (polubień i komentarzy),

przetwarzanie zdarzeń w czasie rzeczywistym,

agregację danych dla poszczególnych hashtagów,

tworzenie rankingu najpopularniejszych hashtagów,

analizę trendów w oknie czasowym (24h),

interaktywną obsługę systemu poprzez aplikację CLI.

Projekt skupia się na wykorzystaniu różnych struktur danych Redis oraz na uzasadnieniu ich zastosowania w kontekście systemów analitycznych czasu rzeczywistego.

2. Uzasadnienie wyboru bazy Redis

Redis jest bazą danych typu key-value, zaliczaną do systemów NoSQL. Dane przechowywane są w pamięci operacyjnej (in-memory), co zapewnia bardzo wysoką wydajność operacji odczytu i zapisu.

Redis został wybrany z następujących powodów:

bardzo szybkie operacje (złożoność O(1) dla wielu struktur),

wsparcie dla wielu typów danych (Strings, Hashes, Sorted Sets, Streams),

natywna obsługa TTL (Time To Live),

możliwość przetwarzania strumieni zdarzeń w czasie rzeczywistym (Redis Streams),

prostota integracji z Pythonem (biblioteka redis-py),

możliwość uruchomienia w środowisku Docker.

W kontekście analizy trendów w czasie rzeczywistym Redis jest szczególnie odpowiedni, ponieważ umożliwia szybkie inkrementowanie liczników oraz dynamiczne tworzenie rankingów bez konieczności wykonywania kosztownych zapytań agregujących.

3. Architektura systemu
3.1 Ogólny schemat działania

System działa według następującego schematu:

Generowanie zdarzeń (like / comment).

Zapis zdarzeń do Redis Stream.

Odczyt nowych zdarzeń przez proces konsumenta.

Agregacja danych w strukturach Hash.

Aktualizacja rankingów w Sorted Set.

Udostępnienie wyników poprzez aplikację CLI.

Schemat logiczny:

Event → Stream → Consumer → Agregacja → Ranking → Odczyt

4. Struktury danych Redis wykorzystane w projekcie
4.1 Redis Streams

Klucz:

stream:events

Wykorzystywane komendy:

XADD

XRANGE

XLEN

Każde zdarzenie zawiera pola:

type (like / comment)

hashtag

user_id

timestamp

Strumień pełni rolę logu zdarzeń i umożliwia przetwarzanie danych w czasie rzeczywistym.

4.2 Hash (agregacja danych)

Klucz:

hashtag:{tag}

Pola:

likes

comments

count

Wykorzystywane komendy:

HINCRBY

HGET

HGETALL

Hash przechowuje zagregowane dane dla pojedynczego hashtagu.
Zastosowanie Hash umożliwia przechowywanie powiązanych wartości w jednym kluczu, co jest bardziej spójne niż użycie wielu oddzielnych kluczy typu String.

4.3 Sorted Sets (rankingi)

Klucze:

ranking:hashtags
ranking:hashtags:24h

Wykorzystywane komendy:

ZINCRBY

ZREVRANGE

ZCARD

ZSCORE

Sorted Set umożliwia przechowywanie elementów wraz z wartością liczbową (score).
Score jest obliczany jako:

like = 1 punkt

comment = 2 punkty

Dzięki temu ranking uwzględnia wagę interakcji.

4.4 TTL (Time To Live)

Wykorzystywane komendy:

EXPIRE

TTL

Ranking 24h posiada ustawiony czas wygaśnięcia.
Po upływie określonego czasu dane są automatycznie usuwane, co pozwala symulować analizę trendów w określonym oknie czasowym (fixed time window).

4.5 Pozostałe operacje Redis

W projekcie wykorzystano również:

GET / SET – zapamiętanie ostatniego przetworzonego ID,

FLUSHALL – czyszczenie bazy (opcjonalnie z menu),

DELETE – usuwanie rankingu 24h.

5. Funkcjonalności aplikacji

Aplikacja posiada interfejs CLI umożliwiający:

Generowanie danych

generowanie N losowych zdarzeń,

generowanie N zdarzeń dla konkretnego hashtagu,

ręczne dodanie pojedynczego zdarzenia.

Przetwarzanie

przetworzenie nowych zdarzeń ze streamu,

inkrementacja liczników,

aktualizacja rankingów.

Analiza

wyświetlenie TOP N hashtagów (globalnie),

wyświetlenie TOP N hashtagów (24h),

wyświetlenie statystyk konkretnego hashtagu,

lista wszystkich śledzonych hashtagów.

System

reset rankingu 24h,

wyświetlenie informacji systemowych (liczba eventów, TTL, ostatnie ID),

bezpieczne czyszczenie bazy (Flush ALL z potwierdzeniem).

6. Analiza trendów

System umożliwia:

analizę popularności hashtagów w czasie rzeczywistym,

porównanie rankingu globalnego i 24h,

obserwację wygasania danych czasowych,

dynamiczne przeliczanie rankingu na podstawie wag interakcji.

Różnica między rankingiem globalnym a 24h pozwala na analizę zmiany popularności w czasie.

7. Technologie wykorzystane w projekcie

Redis

Docker

Python 3

redis-py

CLI (interfejs terminalowy)


8. Podsumowanie

Projekt pokazuje praktyczne zastosowanie bazy NoSQL Redis do analizy danych w czasie rzeczywistym.

Wykorzystanie różnych struktur danych (Streams, Hash, Sorted Sets, TTL) umożliwiło stworzenie wydajnego systemu analitycznego bez konieczności użycia relacyjnej bazy danych.

System jest skalowalny, modularny i umożliwia dalszą rozbudowę o kolejne funkcjonalności analityczne.
