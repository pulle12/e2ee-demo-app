import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class Sender:
    def __init__(self, receiver_public_key):
        self.__receiver_public_key = receiver_public_key

    def send_message(self, original_message):
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
                label=None
            )
        )
        print("[+] Sender: Nachricht und Session-Key wurden verschlüsselt.")

        # --- SIMULIERTER NETZWERK-TRANSPORT (SERVER) ---
        # Der Server sieht nur diese unleserlichen Daten:
        payload_on_server = {
            "encrypted_key": base64.b64encode(encrypted_session_key).decode(),
            "encrypted_message": encrypted_message.decode()
        }
        print(f"[Server-Sicht]: {payload_on_server}")

        return payload_on_server