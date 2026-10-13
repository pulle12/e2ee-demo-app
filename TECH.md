# Technical Architecture & Security Concepts

## Architecture
The application consists of three main components:
1. **Sender Client:** Generates keys, encrypts payload using the recipient's public key / symmetric key, and sends ciphertext.
2. **Relay Server (Mock):** Handles transport of encrypted payloads; has zero access to decryption keys.
3. **Receiver Client:** Uses its local private key to decrypt incoming ciphertext.

## Cryptographic Concepts
- **Symmetric Encryption (AES / Fernet):** Used to encrypt the actual message body efficiently.
- **Asymmetric Encryption (RSA):** Used for exchanging or wrapping symmetric keys securely between clients.
- **Key Storage:** Private keys are stored locally in memory or secure local files, never sent over the network.

## Tech Stack
- **Language:** Python 3.10+
- **Library:** `cryptography` (Python standard-compliant cryptographic recipes)
- **Data Format:** JSON / Base64-encoded strings for message transport