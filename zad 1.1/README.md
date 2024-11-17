# Zad.1.1

Ten katalog zawiera implementacje systemu klient-serwer wykorzystującego protokół UDP. Kod został napisany w dwóch językach programowania: Python i C++. Dla każdego z nich przygotowano osobne Dockerfile.

---

## Struktura katalogów

- **`client_cpp/`**  
  - `client.cpp`: Kod źródłowy klienta napisanego w C++.
  - `Dockerfile`: Plik Docker do budowy obrazu dla klienta C++.

- **`client_python/`**  
  - `client.py`: Kod źródłowy klienta napisanego w Pythonie.
  - `Dockerfile`: Plik Docker do budowy obrazu dla klienta Python.

- **`server_cpp/`**  
  - `server.cpp`: Kod źródłowy serwera napisanego w C++.
  - `Dockerfile`: Plik Docker do budowy obrazu dla serwera C++.

- **`server_python/`**  
  - `server.py`: Kod źródłowy serwera napisanego w Pythonie.
  - `Dockerfile`: Plik Docker do budowy obrazu dla serwera Python.

- **`docker-compose.yml`**  
  - Plik konfiguracyjny Docker Compose do uruchomienia środowiska klient-serwer.

- **`[PSI]Z36_Zad1.1_Sprawozdanie.pdf`**  
  - Sprawozdanie z wynikami zadania.

---

## Jak uruchomić środowisko?

### 1. Wymagania

- **Docker** i **Docker Compose** zainstalowane na komputerze.
- Obrazy używane w projekcie:
  - `python:3-slim` dla implementacji w Pythonie.
  - `gcc:4.9` dla implementacji w C++.

### 2. Budowanie kontenerów Docker

Aby zbudować kontenery Docker dla klienta i serwera, w głównym katalogu wystarczy wykonać polecenie:
```bash
docker-compose up --build
```
Opcja `--build` nie jest konieczna - jeżeli istaniły już kontenery to ta opcja sprawi że zostaną zbudowane od nowa.


To powinno wystarczyć na środowisku `bigubu`, na którym istnieją już sieci dockerowe,
natomiast gdy takich nie posiadamy należy je stworzyć:
```bash
docker network create `
  --driver "bridge" `
  --subnet "172.21.36.0/24" `
  z36_network
```

### 3. Zmiana rodzaju klienta i serwera

W pliku `docker-compose.yml` są zakomentowane pola `context`. Pozawalają one na wybranie, której wersji klienta i serwera chcemy użyć.

---