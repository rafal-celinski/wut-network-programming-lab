import socket

IP = "172.21.36.2"
UDP_PORT = 5018

print(f"Server listening on {IP}:{UDP_PORT}")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    expected_message_bit = 0
    s.bind((IP, UDP_PORT))
    while True:
        message, addr = s.recvfrom(256)
        message = message.decode()
        message_bit = int(message[0])
        iteration = int(message[1:])
        print(f'Received message: Message bit = {message_bit} Iteration = {iteration}')

        if(message_bit == expected_message_bit):
            ack_bit = str(message_bit).encode()
            s.sendto(ack_bit, addr)
            print(f'Send ACK: {message_bit}')
            expected_message_bit = 1 - expected_message_bit
        
        else:
            ack_bit = str(1 - expected_message_bit).encode()
            s.sendto(ack_bit, addr)
            print(f'Resending ACK: {1 - expected_message_bit}')
        