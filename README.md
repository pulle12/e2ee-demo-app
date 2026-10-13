# Cryptographic E2EE Demo App

A lightweight Python prototype demonstrating End-to-End Encryption (E2EE) principles for secure messaging.

## Overview
This project simulates secure communication between two clients over a server. Messages are encrypted on the sender's device using symmetric and asymmetric encryption concepts before transmission, ensuring that only the intended recipient can decrypt and read them.

## Features
- **Client-Side Encryption:** Encryption/decryption happens strictly on the local device.
- **Hybrid Encryption Concept:** Demonstrates public-key cryptography for key exchange and symmetric encryption for fast payload transfer.
- **Zero-Knowledge Relay:** The central server acts purely as a message broker without access to plaintext data or private keys.

## Quickstart
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/e2ee-demo-app.git](https://github.com/your-username/e2ee-demo-app.git)
   cd e2ee-demo-app
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the demo:**
   ```bash
   python main.py
   ```

