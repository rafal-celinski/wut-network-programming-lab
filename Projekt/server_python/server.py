import socket
import argparse
import json
import threading

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--private_key", type=int)

args = parser.parse_args()

IP = "172.21.36.2"
TCP_PORT = 8080

PRIVATE_KEY = args.private_key

CLIENTS = {} 
CLIENTS_READY = {}
CLIENTS_LOCK = threading.Lock()


def handle_serving_clients(server_socket: socket.socket):
    while True:
        conn, addr = server_socket.accept()
        print(f"Client connected: {addr}")
        addr_str = f"{addr[0]}:{addr[1]}"
        with CLIENTS_LOCK:
            CLIENTS[addr_str] = conn
            CLIENTS_READY[addr_str] = False
        client_thread = threading.Thread(target=handle_client, args=(conn, addr_str, PRIVATE_KEY,))
        client_thread.daemon = True
        client_thread.start()


def handle_client(conn, addr_str, private_key):
    while True:
        data = conn.recv(1024)
        with CLIENTS_LOCK:
            if not CLIENTS_READY[addr_str]:      
                try:
                    message = json.loads(data.decode('utf-8'))
                    if "type" in message and message["type"] == "Hello message":
                        print(f"Received Hello Message from {addr_str}: {message}")  
                        CLIENTS_READY[addr_str] = True
                        public_key = (message["base"] ** private_key) % message["modulus"]
                        response = {
                            "type": "Hello message",
                            "public_key": public_key
                        }
                        conn.sendall(json.dumps(response).encode('utf-8'))
                        print(f"Sent Hello Message response to {addr_str}")
                    else:
                        print(f"Received message from {addr_str}, but ignoring until Hello Message.")
                except json.JSONDecodeError:
                    print(f"Received message from {addr_str}, but ignoring until Hello Message.")
            else:
                message = data.decode('utf-8')
                if message == "EndSession":
                    print(f'Session ended by {addr_str}. Can''t send messages there')
                    CLIENTS_READY[addr_str]= False
                else:
                    print(f'Received normal message from {addr_str}: {message}')

            

def send_message_to_client(client_ip, message):
    with CLIENTS_LOCK:
        if client_ip in CLIENTS_READY and CLIENTS_READY[client_ip]:
            conn = CLIENTS[client_ip]
            conn.sendall(message.encode('utf-8'))
            if message == "EndSession":
                print(f'Ending connection with {client_ip}')
                CLIENTS_READY[client_ip] = False
            else:
                print(f"Sent message to {client_ip}: {message}")
        else:
            print(f"No active connection to {client_ip}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((IP, TCP_PORT))
    server_socket.listen()
    print(f"Server listening on {IP}:{TCP_PORT}")

    serving_clients_thread = threading.Thread(target=handle_serving_clients, args=(server_socket,))
    serving_clients_thread.daemon = True
    serving_clients_thread.start()

    while True:
        print("Clients ready for messages: ", CLIENTS_READY)
        client_ip = input("Enter client IP to send message to:\n")
        message = input("Enter message to send:\n")

        send_message_to_client(client_ip, message)


