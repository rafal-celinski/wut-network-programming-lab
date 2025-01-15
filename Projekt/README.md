# Projekt

Ten katalog zawiera implementację projektu szyfrowanego protokołu opartego na protokole TCP. Kod został napisany w Pythonie. Dla serwera i klienta przygotowano Dockerfile.

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

- **`Sprawozdanie_początkowe.pdf`**  
  - Plan projektu.
  
- **`Sprawozdanie_końcowe.pdf`**  
  - Zaimplementowany projekt wraz z wynikami testów.
  
- **`manual_decryption.py`**
  - Ręcznie zaimplementowane odszyfrowanie wiadomości. Więcej informacji w Sprawozdaniu Końcowym.

---

## Jak uruchomić środowisko?

### 1. Wymagania

- **Docker** i **Docker Compose** zainstalowane na komputerze.
- Obrazy używane w projekcie:
  - `python:3-slim` dla implementacji w Pythonie.

### 2. Budowanie kontenerów Docker

Aby zbudować obrazy dla kontenerów Docker dla klienta i serwera, w głównym katalogu wystarczy wykonać polecenie:
```bash
docker-compose build
```

Następnie należy uruchomić serwer:
```bash
 docker-compose run --rm  z36_server -k 10
```
Użycie parametru `--rm` sprawi, że kontener zostanie usunięty po zakończeniu działania
Parametr `k` oznacz wartość klucza prywatnego używanego w szyfrowaniu
Po wpisaniu tej komendy automatycznie włączy się terminal kontenera

Aby uruchomić kontener klienta:
```bash
docker run -it --rm --name z36_client1_container --network z36_network --ip 172.21.36.3 z36_client_image -b 7 -m 31 -k 17
```
Wszystkie parametry ustawiane są ręcznie ponieważ korzystamy tutaj z polecenia `docker run`
Jest to spowodowane tym, że nigdzie nie narzucamy odgórnie maksymalnej ilości klientów, dlatego tworzymy ich kontenery w ten sposób.
Z komendą należy się bezpiecznie obchodzić, szczególnie w środowisku takim jak `bigubu` żeby przypadkiem nie podłączyć kontenera do przypadkowej sieci, a
także należy uważać na ustawione `ip`.

Przy tworzeniu kolejnych kontenerów klienta, należy zmieniać parametr `name`

Jeżeli chcielibyśmy uzyskać inny kontener:
```bash
docker run -it --rm --name z36_client2_container --network z36_network --ip 172.21.36.4 z36_client_image -b 3 -m 17 -k 15
```

Należy pamiętać, że adresy `172.21.36.1, 172.21.36.2` są już zarezerwowane.

Dodatkowe parametry używane przy tworzeniu kontenerów klienta:
`-b` - baza, używana do obliczania klucza publicznego, wysyłana do kontenera serwera w ramach algorytmu Diffiego-Hellmana
`-m` - moduł, używany do obliczania klucza publicznego i wspólnego, wysyłana do kontenera serwera w ramach algorytmu Diffiego-Hellmana
`-k` - klucz prywatny

To powinno wystarczyć na środowisku `bigubu`, na którym istnieją już sieci dockerowe,
natomiast gdy takich nie posiadamy należy je stworzyć:
```bash
docker network create `
  --driver "bridge" `
  --subnet "172.21.36.0/24" `
  z36_network
```

Plik `manual_decryption.py` jest zwykłym pythonowym plikiem i w przypadku sprawdzania jego działania należy go uruchomić tak jak każdy inny plik `.py`