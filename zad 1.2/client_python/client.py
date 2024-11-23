import socket
import time

HOST = "172.21.36.2"
UDP_PORT = 5018

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    iteration = 0
    while True:
        message = f"{iteration}: Test message".encode()
        try:
            sent_bytes = s.sendto(message, (HOST, UDP_PORT))
            print(f"Sent message: {iteration}")
        except Exception as e:
            print(f"Couldn't send message: {iteration}")
            continue
        iteration = iteration + 1
        time.sleep(0.2)

s.close()


