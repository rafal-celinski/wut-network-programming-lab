import argparse
import socket
import json
import threading
import sys
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--base", type=int)
parser.add_argument("-m", "--modulus", type=int)
parser.add_argument("-k", "--private_key", type=int)

args = parser.parse_args()

HOST = "172.21.36.2"
TCP_PORT = 8080

BASE = args.base
MODULUS = args.modulus
PRIVATE_KEY = args.private_key
PUBLIC_KEY = (BASE**PRIVATE_KEY) % MODULUS
SHARED_KEY = -1

RECEIVED_HELLO = False
HELLO_LOCK = threading.Lock()

def encrypt_message(message):
    expanded_key = SHA256.new(str(SHARED_KEY).encode('utf-8')).digest()
    print(SHARED_KEY)
    
    
    iv = get_random_bytes(16)
    cipher = AES.new(expanded_key, AES.MODE_CBC, iv)
    
    padding_length = 16 - (len(message) % 16)
    padded_message = message + chr(padding_length) * padding_length
    
    ciphertext = cipher.encrypt(padded_message.encode('utf-8'))
    
    hmac = HMAC.new(expanded_key, digestmod=SHA256)
    hmac.update(iv + ciphertext)

    print(f"IV: {iv}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Computed HMAC: {hmac.digest()}")
    
    final_message = iv + ciphertext + hmac.digest()
    print(final_message)
    
    return final_message


def decrypt_message(encrypted_message):
    iv = encrypted_message[:16]  
    ciphertext = encrypted_message[16:-32]  
    received_hmac = encrypted_message[-32:]  
    

    expanded_key = SHA256.new(str(SHARED_KEY).encode('utf-8')).digest()
    

    hmac = HMAC.new(expanded_key, digestmod=SHA256)
    hmac.update(iv + ciphertext)
    try:
        hmac.verify(received_hmac)
    except ValueError:
        raise ValueError("Invalid MAC")

    cipher = AES.new(expanded_key, AES.MODE_CBC, iv)
    

    decrypted_data = unpad(cipher.decrypt(ciphertext), 16)  
    return decrypted_data.decode('utf-8')


def handle_server_messages(server_socket: socket.socket):
    global RECEIVED_HELLO
    global SHARED_KEY
    while True:
        response = server_socket.recv(1024)

        if not response:
            print("Server has closed the connection. Exiting client.")
            server_socket.close()
            sys.exit(0)

        with HELLO_LOCK:
            if not RECEIVED_HELLO:
                try:
                    response_message = json.loads(response.decode('utf-8'))
                    if "type" in response_message and response_message["type"] == "Hello message":
                        RECEIVED_HELLO = True
                        SHARED_KEY = (response_message["public_key"]**PRIVATE_KEY) % MODULUS
                        print("Received Hello Message from server")
                        # print("Shared_key: ", SHARED_KEY)
                    else:
                        print("Expected Hello Message, got something else.")
                except json.JSONDecodeError:
                    print("Expected Hello Message, got something else.")
            else:
                message = decrypt_message(response)
                if message == "EndSession":
                    print("Session ended by server. To initiate it again send ClientHello")
                    RECEIVED_HELLO = False
                else:
                    print(f'Received normal message from server: {message}')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, TCP_PORT))
    except ConnectionRefusedError:
        print(f"Could not connect to server {HOST}:{TCP_PORT}. Is the server running?")
        sys.exit(1)

    print(f'Connected to server {HOST}:{TCP_PORT}')
    server_thread = threading.Thread(target=handle_server_messages, args=(s,))
    server_thread.daemon = True
    server_thread.start()
    
    try:
        while True:
            command_id = input("Available options:\n-1 - Send Hello Message to server\n-2 - Send message\n-3 - Send EndSession\n")
            if command_id == "1":
                with HELLO_LOCK:
                    if RECEIVED_HELLO:
                        print("Session is active, no need to send that message again")
                    else:
                        message = {
                            "type": "Hello message",
                            "public_key": PUBLIC_KEY,
                            "base": BASE,
                            "modulus": MODULUS
                        }
                        s.sendall(json.dumps(message).encode('utf-8'))
                        print(f"Sent Hello Message to server")
                        RECEIVED_HELLO = False
            elif command_id == "2":
                message = input("Type message content: ")
                encypted_message = encrypt_message(message)
                with HELLO_LOCK:
                    if not RECEIVED_HELLO:
                        print("Session is not active, message won't be sent")
                    elif message == "EndSession":
                        s.sendall(encypted_message)
                        print("Ended session - to initiate it again send Hello Message")
                        RECEIVED_HELLO = False
                    else: 
                        s.sendall(encypted_message)
                        print("Sent normal message")
            elif command_id == "3":
                message = "EndSession"
                encypted_message = encrypt_message(message)
                with HELLO_LOCK:
                    if RECEIVED_HELLO:
                        s.sendall(encypted_message)
                        print("Ended session - to initiate it again send ClientHello")
                        RECEIVED_HELLO = False
                    else:
                        print("Session is not active, message won't be sent")
            else:
                print("Invalid option. Please try again.")
    except KeyboardInterrupt:
        print("\nClient shutting down.")
        s.close()
