import socket
import time

HOST = "172.21.36.2"
UDP_PORT = 5018

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    len = 4
    message_size = 2
    failed_send = False
    found_max = False
    while True:
        # Pierwsze 4 bajty reprezentują długość datagramu
        message = bytearray(message_size + len)
        message[:len] = message_size.to_bytes(len, byteorder='little')

        # W reszcie wiadomości ustawiamy powtarzające się literry alfabetu
        for i in range(len, message_size + len):
            message[i] = 65 + (i % 26)

        # Wysłanie datagramu
        try:
            sent_bytes = s.sendto(message, (HOST, UDP_PORT))
            print(f"Size of sent message: {message_size} bytes, whole datagram size: {message_size + len}")
            if(failed_send):
                found_max = True
        except Exception as e:
            failed_send = True
            print(f"Couldn't send message of size: {message_size + len} bytes")
            message_size -= 1
            time.sleep(0.2)
            continue

        # Odebranie odpowiedzi
        try:
            data, address = s.recvfrom(1024)
            if data:
                print(f"Received answer: {data.decode()}")
                if data.decode() != "OK":
                    print("Invalid packet recevied on server side, sending message with same size.")
                    time.sleep(0.5)
                    continue
        except socket.timeout:
            print("Timeout")

        if(found_max):
            print(f"Maximum datagram size sent: {message_size + len}, message size: {message_size}")
            break    

        message_size *= 2
        time.sleep(0.5)

    s.close()


