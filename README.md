# RFID Key Management System

This project contains both the server and client code for managing RFID keys through Telegram and an Arduino-based RFID reader.

---

## Repository Structure

```
/
├── client/      # Arduino code (RFID reader client)
├── server/      # Python Flask + Telegram bot server
├── requirements.txt
└── README.md
```

---

## Server (Python)

The server exposes:
- A **Telegram Bot** for interacting with users.
- A **Flask HTTP API** to accept key validations or registrations from the client.

### How to Set Up the Server

1. **Install dependencies**:

   ```bash
   cd server
   pip install -r ../requirements.txt
   ```

2. **Configuration**:
   
   Create a `configuration.py` inside `server/` with the following content:

   ```python
   TELEGRAM_API_KEY = "your-telegram-bot-api-key"

   known_keys = []  # This will temporarily store registered keys
   ```

3. **Run the server**:

   ```bash
   python server.py
   ```

   The server will:
   - Start polling Telegram for messages.
   - Listen on HTTP port `5000` for `/iskeyvalid` requests.

---

## Client (Arduino)

The client runs on an **Arduino** equipped with:
- An **RFID reader**.
- (Optionally) a **WiFi/Ethernet module** to send HTTP requests.

### Client Behavior

- When a card is scanned:
  - The Arduino sends a GET request to the `/iskeyvalid?id=<CARD_ID>` endpoint.
  - Based on the server's response:
    - `'g'` ➔ Key is known ➔ Access granted.
    - `'r'` ➔ Key is unknown ➔ Access denied.
    - `'a'` ➔ Key added (if in key registration mode).

(You can find the Arduino source code inside `client/`.)

---

## Quick Commands (Telegram)

Once your bot is running, you can use these commands:

- `/newkey` → Start a 30-second window to register a new RFID key.

When prompted, scan the RFID card to register it.
