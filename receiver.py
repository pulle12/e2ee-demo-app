import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class Receiver:
    def __init__(self):
        # Empfänger generiert sein RSA-Schlüsselpaar (Public & Private Key)
        self.__receiver_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.__receiver_public_key = self.__receiver_private_key.public_key()
        print("[+] Empfänger: RSA-Schlüsselpaar generiert.")

        # Empfänger speichert seine Private Key sicher (z.B. in einem lokalen Passwort-Manager wie KeePass oder am optimalsten auf einem Hardware-Sicherheitsschlüssel wie YubiKey)
        # Der Schritt wird hier ausgelassen in der Demo.
        print("[*] Empfänger: Private Key wird sicher gespeichert.")

    def get_public_key(self):
        # Empfänger teilt seinen Public Key mit dem Sender (z.B. in der Praxis über einen öffentlichen Key-Server)
        return self.__receiver_public_key

    def decrypt_message(self, payload_on_server):
        # Empfänger entschlüsselt zuerst den Session-Key mit seinem Private Key
        decrypted_session_key = self.__receiver_private_key.decrypt(
            base64.b64decode(payload_on_server["encrypted_key"]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Empfänger entschlüsselt die Nachricht mit dem entschlüsselten Session-Key
        receiver_cipher_suite = Fernet(decrypted_session_key)
        decrypted_message = receiver_cipher_suite.decrypt(payload_on_server["encrypted_message"].encode())

        print(f"[<] Empfänger Entschlüsselt: '{decrypted_message.decode()}'")
