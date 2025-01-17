from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

SERVER_PRIVATE_KEY = 10
CLIENT_PRIVATE_KEY = 15
BASE = 5
MODULUS = 23

server_public_key = (BASE**SERVER_PRIVATE_KEY) % MODULUS
client_public_key = (BASE**CLIENT_PRIVATE_KEY) % MODULUS
print(f'Server public key: {server_public_key}')
print(f'Client public key: {client_public_key}')

shared_key_by_server = (client_public_key**SERVER_PRIVATE_KEY) % MODULUS
shared_key_by_client = (server_public_key**CLIENT_PRIVATE_KEY) % MODULUS
print(f'Shared key calculated by server: {shared_key_by_server}')
print(f'Shared key calculated by client: {shared_key_by_client}')

shared_key = shared_key_by_server #Są takie same

hex_message = "b53a1663be2334120bf6c7e07d92936e0227849e0490465497ed963b9e36646cf834b2df708a7a2fa6e2023b51710007823b46d6c67305cc37ffd8473dd370df386d62a1914cec641d2e24e94ccde48bdc82444311c47cda58ecfe06218c19e9c5f5c16ac1f92dcc8a5a41d90a107910c4f2cd05977013dca5ba74feb7151a42"

encrypted_message = bytes.fromhex(hex_message)

iv = encrypted_message[:16]  
ciphertext = encrypted_message[16:-32]  
received_hmac = encrypted_message[-32:]  
expanded_key = SHA256.new(str(shared_key).encode('utf-8')).digest()

hmac = HMAC.new(expanded_key, digestmod=SHA256)

hmac.update(iv + ciphertext)
print(f"IV: {iv}")
print(f"Ciphertext: {ciphertext}")
print(f"Received HMAC: {received_hmac}")
print(f"Computed HMAC: {hmac.digest()}")
try:
    hmac.verify(received_hmac)
except ValueError:
    raise ValueError("Invalid MAC")

cipher = AES.new(expanded_key, AES.MODE_CBC, iv)


decrypted_data = unpad(cipher.decrypt(ciphertext), 16)  
print(decrypted_data.decode('utf-8'))