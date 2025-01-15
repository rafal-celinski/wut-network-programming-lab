import socket
import argparse
import json
import threading
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--private_key", type=int)

args = parser.parse_args()

IP = "172.21.36.2"
TCP_PORT = 8080

PRIVATE_KEY = args.private_key

CLIENTS = {} 
CLIENTS_LOCK = threading.Lock()


def encrypt_message(message, shared_key):
    expanded_key = SHA256.new(str(shared_key).encode('utf-8')).digest()
    
    iv = get_random_bytes(16)
    cipher = AES.new(expanded_key, AES.MODE_CBC, iv)
    
    padding_length = 16 - (len(message) % 16)
    padded_message = message + chr(padding_length) * padding_length
    
    ciphertext = cipher.encrypt(padded_message.encode('utf-8'))
    
    hmac = HMAC.new(expanded_key, digestmod=SHA256)
    hmac.update(iv + ciphertext)
    
    to_send_message = iv + ciphertext + hmac.digest()
    
    return to_send_message


def decrypt_message(encrypted_message, shared_key):
    # print(shared_key)
    # print(encrypted_message)
    iv = encrypted_message[:16]  
    ciphertext = encrypted_message[16:-32]  
    received_hmac = encrypted_message[-32:]  
    

    expanded_key = SHA256.new(str(shared_key).encode('utf-8')).digest()

    hmac = HMAC.new(expanded_key, digestmod=SHA256)

    hmac.update(iv + ciphertext)
    # print(f"IV: {iv}")
    # print(f"Ciphertext: {ciphertext}")
    # print(f"Received HMAC: {received_hmac}")
    # print(f"Computed HMAC: {hmac.digest()}")
    try:
        hmac.verify(received_hmac)
    except ValueError:
        raise ValueError("Invalid MAC")

    cipher = AES.new(expanded_key, AES.MODE_CBC, iv)
    

    decrypted_data = unpad(cipher.decrypt(ciphertext), 16)  
    return decrypted_data.decode('utf-8')


def clients_ready():
    result = ''
    with CLIENTS_LOCK:
        for key in CLIENTS.keys():
            if CLIENTS[key][1]:
                result += f'User at address {key} READY for messages\n'
            else:
                result += f'User at address {key} NOT READY for messages\n'
    return result


def handle_serving_clients(server_socket):
    while True:
        conn, addr = server_socket.accept()
        addr_str = f"{addr[0]}:{addr[1]}"
        print(f"Client connected: {addr_str}")
        with CLIENTS_LOCK:
            CLIENTS[addr_str] = [conn, False, -1]
        client_thread = threading.Thread(target=handle_client, args=(conn, addr_str, PRIVATE_KEY,))
        client_thread.daemon = True
        client_thread.start()


def handle_client(conn, addr_str, private_key):
    while True:
        data = conn.recv(1024)
        if not data:
                print(f'Client {addr_str} has closed the connection.')
                conn.close()
                with CLIENTS_LOCK:
                    del CLIENTS[addr_str]
                break
        with CLIENTS_LOCK:
            if not CLIENTS[addr_str][1]:      
                try:
                    message = json.loads(data.decode('utf-8'))
                    if "type" in message and message["type"] == "Hello message":
                        print(f"Received Hello Message from {addr_str}")  
                        CLIENTS[addr_str][1] = True
                        public_key = (message["base"] ** private_key) % message["modulus"]
                        response = {
                            "type": "Hello message",
                            "public_key": public_key
                        }
                        CLIENTS[addr_str][2] = (message["public_key"]**PRIVATE_KEY) % message['modulus']
                        # print("Shared_key: ", CLIENTS[addr_str][2])
                        conn.sendall(json.dumps(response).encode('utf-8'))
                        print(f"Sent Hello Message response to {addr_str}")
                    else:
                        print(f"Received message from {addr_str}, but ignoring until Hello Message.")
                except json.JSONDecodeError:
                    print(f"Received message from {addr_str}, but ignoring until Hello Message.")
            else:
                message = decrypt_message(data, CLIENTS[addr_str][2])
                if message == "EndSession":
                    print(f'Session ended by {addr_str}. Can''t send messages there')
                    CLIENTS[addr_str][1]= False
                    CLIENTS[addr_str][2]= -1
                else:
                    print(f'Received normal message from {addr_str}: {message}')


def send_message_to_client(client_ip, message):
    with CLIENTS_LOCK:
        if client_ip in CLIENTS and CLIENTS[client_ip][1]:
            conn = CLIENTS[client_ip][0]
            encypted_message = encrypt_message(message, CLIENTS[client_ip][2])
            conn.sendall(encypted_message)
            if message == "EndSession":
                print(f'Ending connection with {client_ip}')
                CLIENTS[client_ip][1] = False
                CLIENTS[client_ip][2]= -1
            else:
                print(f"Sent message to {client_ip}: {message}")
        else:
            print(f"No active connection to {client_ip}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP, TCP_PORT))
    s.listen()
    print(f"Server listening on {IP}:{TCP_PORT}")

    serving_clients_thread = threading.Thread(target=handle_serving_clients, args=(s,))
    serving_clients_thread.daemon = True
    serving_clients_thread.start()
    try:
        print("If you want to print clients connected write `list`, else just type IP:PORT of client you want to connect")
        while True:
            command = input()
            if command == "list":
                print(clients_ready())
            else:
                client_ip = command
                message = input("Enter message to send:\n")
                send_message_to_client(client_ip, message)
    except KeyboardInterrupt:
        s.close()
        


