import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def main():
    print("=== E2EE Demo Simulation ===")

    # 1. Empfänger generiert sein RSA-Schlüsselpaar (Public & Private Key)
    receiver_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    receiver_public_key = receiver_private_key.public_key()
    print("[+] Empfänger: RSA-Schlüsselpaar generiert.")

    # 2. Sender möchte eine Nachricht senden
    original_message = "Hallo, das ist eine vertrauliche Nachricht!".encode('utf-8')
    print(f"[>] Sender Original-Nachricht: '{original_message.decode()}'")

    # 3. Sender erzeugt einen symmetrischen Schlüssel (Fernet/AES) für die Nachricht
    session_key = Fernet.generate_key()
    cipher_suite = Fernet(session_key)
    encrypted_message = cipher_suite.encrypt(original_message)

    # 4. Sender verschlüsselt den symmetrischen Schlüssel mit dem RSA Public Key des Empfängers
    encrypted_session_key = receiver_public_key.encrypt(
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

    # --- EMPFÄNGER-SEITE ---
    # 5. Empfänger entschlüsselt zuerst den Session-Key mit seinem Private Key
    decrypted_session_key = receiver_private_key.decrypt(
        base64.b64decode(payload_on_server["encrypted_key"]),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 6. Empfänger entschlüsselt die Nachricht mit dem entschlüsselten Session-Key
    receiver_cipher_suite = Fernet(decrypted_session_key)
    decrypted_message = receiver_cipher_suite.decrypt(payload_on_server["encrypted_message"].encode())

    print(f"[<] Empfänger Entschlüsselt: '{decrypted_message.decode()}'")

if __name__ == "__main__":
    main()