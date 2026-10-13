import base64
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from websockets.asyncio.client import connect


class Sender:
    def __init__(self, receiver_public_key):
        self.__receiver_public_key = receiver_public_key

    async def send_message(self, original_message):
        # 1. Sender erzeugt einen symmetrischen Schlüssel (Fernet/AES) für die Nachricht
        session_key = Fernet.generate_key()
        cipher_suite = Fernet(session_key)
        encrypted_message = cipher_suite.encrypt(original_message)

        # 2. Sender verschlüsselt den symmetrischen Schlüssel mit dem RSA Public Key des Empfängers
        encrypted_session_key = self.__receiver_public_key.encrypt(
            session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        print("[+] Sender: Nachricht und Session-Key wurden verschlüsselt.")

        uri = "ws://localhost:8765"

        # Verbindung zum Server aufbauen
        async with connect(uri) as websocket:
            payload_on_server = {
                "encrypted_key": base64.b64encode(encrypted_session_key).decode(),
                "encrypted_message": encrypted_message.decode(),
            }

            json_string = json.dumps(payload_on_server, indent=4, ensure_ascii=False)

            print(f"Sende: {json_string}")
            await websocket.send(json_string)

            # Auf die Antwort des Servers warten
            response = await websocket.recv()
            print(f"Empfangen vom Server: {response}")
