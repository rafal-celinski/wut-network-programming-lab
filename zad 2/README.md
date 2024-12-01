# Zadanie 2

Ten katalog zawiera implementacje systemu klient-serwer wykorzystującego protokół TCP. Kod został napisany w C++. Dla klienta i serwera przygotowano osobne Dockerfile.

---

## Struktura katalogów

- **`client_cpp/`**  
  - `client.cpp`: Kod źródłowy klienta napisanego w C++.
  - `Dockerfile`: Plik Docker do budowy obrazu dla klienta C++.

- **`server_cpp/`**  
  - `server.cpp`: Kod źródłowy serwera napisanego w C++.
  - `Dockerfile`: Plik Docker do budowy obrazu dla serwera C++.

- **`docker-compose.yml`**  
  - Plik konfiguracyjny Docker Compose do uruchomienia środowiska klient-serwer.

- **`[PSI]Z36_Zad2_Sprawozdanie.pdf`**  
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