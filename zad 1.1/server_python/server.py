import socket
import time

IP = "172.21.36.2"
UDP_PORT = 5018

print(f"Server listening on {IP}:{UDP_PORT}")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((IP, UDP_PORT))
    while True:
        data, addr = s.recvfrom(100000)
        print(f"Received datagram of size {len(data)} from {addr}")

        message_size = int.from_bytes(data[:4], byteorder='little')

        if message_size + 4 == len(data):
            print(f"Message length validated successfully for message of size {message_size} bytes.")
            s.sendto(b"OK", addr)
        else:
            print(f"Expected {message_size + 4} bytes, got {len(data)}.")
            s.sendto(b"FAIL", addr)