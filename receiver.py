import base64
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from websockets.asyncio.server import serve


class Receiver:
    def __init__(self):
        # Empfänger generiert sein RSA-Schlüsselpaar (Public & Private Key)
        self.__receiver_private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048
        )
        self.__receiver_public_key = self.__receiver_private_key.public_key()
        print("[+] Empfänger: RSA-Schlüsselpaar generiert.")

        # Empfänger speichert seine Private Key sicher (z.B. in einem lokalen Passwort-Manager wie KeePass oder am optimalsten auf einem Hardware-Sicherheitsschlüssel wie YubiKey)
        # Der Schritt wird hier ausgelassen in der Demo.
        print("[*] Empfänger: Private Key wird sicher gespeichert.")

    async def echo(self, websocket):
        print(f"Client verbunden: {getattr(websocket, 'remote_address', 'unknown')}")

        # Warten auf Sender-Client
        async for message in websocket:
            print(f"Empfangen: {message}")

            # Entschlüsselung muss immer erfolgen, bevor die Nachricht weiterverarbeitet wird.
            self.decrypt_message(message)

            # Antwort zurück an den Client senden
            response = f"Server-Echo: {message}"
            await websocket.send(response)
            return message

    async def start_server(self):
        self._server = await serve(self.echo, "localhost", 8765)
        print("WebSocket-Server läuft auf ws://localhost:8765")
        return self._server

    async def get_public_key(self):
        return self.__receiver_public_key

    def decrypt_message(self, payload_on_server):
        # Empfänger entschlüsselt zuerst den Session-Key mit seinem Private Key

        neues_dict = json.loads(payload_on_server)

        decrypted_session_key = self.__receiver_private_key.decrypt(
            base64.b64decode(neues_dict["encrypted_key"]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # Empfänger entschlüsselt die Nachricht mit dem entschlüsselten Session-Key
        receiver_cipher_suite = Fernet(decrypted_session_key)
        decrypted_message = receiver_cipher_suite.decrypt(
            neues_dict["encrypted_message"].encode()
        )

        print(f"[<] Empfänger Entschlüsselt: '{decrypted_message.decode()}'")
