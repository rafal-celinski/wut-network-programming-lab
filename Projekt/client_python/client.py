import argparse
import socket
import json
import threading
import sys

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

RECEIVED_HELLO = False
HELLO_LOCK = threading.Lock()

def handle_server_messages(server_socket: socket.socket):
    global RECEIVED_HELLO
    while True:
        try:
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
                            print("Received Hello Message")
                        else:
                            print("Expected Hello Message, got something else.")
                    except json.JSONDecodeError:
                        print("Expected Hello Message, got something else.")
                else:
                    response_message = response.decode('utf-8')
                    if response_message == "EndSession":
                        print("Session ended by server. To initiate it again send ClientHello")
                        RECEIVED_HELLO = False
                    else:
                        print(f'Received normal message from server: {response_message}')
        except (ConnectionResetError, ConnectionAbortedError):
            print("Server has forcibly closed the connection. Exiting client.")
            server_socket.close()
            sys.exit(0)


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
                with HELLO_LOCK:
                    if not RECEIVED_HELLO:
                        print("Session is not active, message won't be sent")
                    elif message == "EndSession":
                        s.sendall(message.encode('utf-8'))
                        print("Ended session - to initiate it again send Hello Message")
                        RECEIVED_HELLO = False
                    else: 
                        s.sendall(message.encode('utf-8'))
                        print("Sent normal message")
            elif command_id == "3":
                message = "EndSession"
                with HELLO_LOCK:
                    s.sendall(message.encode('utf-8'))
                    print("Ended session - to initiate it again send ClientHello")
                    RECEIVED_HELLO = False
            else:
                print("Invalid option. Please try again.")
    except KeyboardInterrupt:
        print("\nClient shutting down.")
    finally:
        s.close()
        print("Socket closed. Exiting client.")
