import asyncio

from receiver import Receiver
from sender import Sender


async def main():
    print("=== E2EE Demo Simulation ===")

    receiver = Receiver()  # Schlüsselpaar wird im Konstruktor generiert.

    # Empfänger teilt seinen Public Key mit dem Sender (z.B. über einen öffentlichen Key-Server)
    # Hier wird einfach der Public Key direkt im Code über einen Getter mitgeteilt.
    print("[*] Empfänger: Public Key wird mit dem Sender geteilt.")

    server = await receiver.start_server()
    receiver_public_key = await receiver.get_public_key()
    sender = Sender(receiver_public_key)  # Sender erhält den Public Key des Empfängers.
    original_message = b"Hallo, das ist eine vertrauliche Nachricht!"
    print(f"[>] Sender Original-Nachricht: '{original_message.decode()}'")

    await sender.send_message(original_message)

    server.close()
    await server.wait_closed()


asyncio.run(main())
