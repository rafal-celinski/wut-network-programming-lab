import socket
import time

IP = "172.21.36.2"
UDP_PORT = 5018

print(f"Server listening on {IP}:{UDP_PORT}")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((IP, UDP_PORT))
    while True:
        data, addr = s.recvfrom(256)
        print(f"Received datagram: {data.decode()}")