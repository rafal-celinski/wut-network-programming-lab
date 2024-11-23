import socket
import time

HOST = "172.21.36.2"
UDP_PORT = 5018

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(2)
    message_bit = 0
    for iteration in range(2000):
        message = f"{message_bit}{iteration}".encode()
        while True:
            sent_bytes = s.sendto(message, (HOST, UDP_PORT))
            print(f"Sent message: Message bit = {message_bit}, Iteration = {iteration}")
            try:
                ack_bit, address = s.recvfrom(256)
                ack_bit = int(ack_bit.decode())
                print(f'Received ACK: {ack_bit}')
                if (ack_bit == message_bit):
                    message_bit = 1 - message_bit
                    break
            except socket.timeout:
                print("No ACK. Resending.")
        time.sleep(0.2)

s.close()


