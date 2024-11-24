# Zadanie 1.2

Ten katalog zawiera implementacje systemu klient-serwer wykorzystującego protokół UDP wraz z algorytmem `bit alternate protocol`. Kod został napisany w Pythonie. Dla serwera i klienta przygotowano Dockerfile.

---

## Struktura katalogów

- **`client_python/`**  
  - `client.py`: Kod źródłowy klienta napisanego w Pythonie.
  - `Dockerfile`: Plik Docker do budowy obrazu dla klienta Python.

- **`server_python/`**  
  - `server.py`: Kod źródłowy serwera napisanego w Pythonie.
  - `Dockerfile`: Plik Docker do budowy obrazu dla serwera Python.

- **`docker-compose.yml`**  
  - Plik konfiguracyjny Docker Compose do uruchomienia środowiska klient-serwer.

- **`[PSI]Z36_Zad1.2_Sprawozdanie.pdf`**  
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

### 3. Wprowadzanie zakłóceń w środowisku

Żeby zasymulować warunki gubienia pakietów, na drugim terminalu (na pierwszym uruchamiamy kontenery i obserwujemy to co zwracają na programy) trzeba uruchomić polecenia
```bash
docker exec z36_client_container tc qdisc add dev eth0 root netem loss 40%
docker exec z36_server_container tc qdisc add dev eth0 root netem loss 40%
```

---