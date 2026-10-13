from receiver import Receiver
from sender import Sender

print("=== E2EE Demo Simulation ===")

receiver = Receiver() # Schlüsselpaar wird im Konstruktor generiert.

# Empfänger teilt seinen Public Key mit dem Sender (z.B. über einen öffentlichen Key-Server)
# Hier wird einfach der Public Key direkt im Code über einen Getter mitgeteilt.
print("[*] Empfänger: Public Key wird mit dem Sender geteilt.")

receiver_public_key = receiver.get_public_key()
sender = Sender(receiver_public_key) # Sender erhält den Public Key des Empfängers.
original_message = "Hallo, das ist eine vertrauliche Nachricht!".encode('utf-8')
print(f"[>] Sender Original-Nachricht: '{original_message.decode()}'")
payload = sender.send_message(original_message)
receiver.decrypt_message(payload) # Empfänger entschlüsselt die Nachricht.