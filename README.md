# ESP32-S2 Mini HTTP Monitor + Telegram Alerts

![ESP32-S2](https://img.shields.io/badge/Board-ESP32--S2%20Mini-blue)
![MicroPython](https://img.shields.io/badge/Firmware-MicroPython-orange)
![License](https://img.shields.io/badge/License-MIT-green)
[BOARD WEMOS]([https://www.wemos.cc/en/latest/s2/s2_mini.html](https://www.aliexpress.com/item/1005003145192016.html))

Minimal IoT monitor for ESP32-S2 Mini that checks HTTP/HTTPS endpoints and sends Telegram alerts.
---
<img width="797" height="798" alt="image" src="https://github.com/user-attachments/assets/32cf63ed-a546-43a4-87ba-81857792f36f" />

---

## 📦 Hardware

- **Board**: Wemos ESP32-S2 Mini v1.0.0 (or any ESP32-S2)[](https://www.wemos.cc/en/latest/s2/s2_mini.html)
- **LED**: Onboard GPIO 15 (or 18)
- **Power**: USB-C cable (WiFi needs stable power)

---

## ⚡ Quick Setup

1. **Flash MicroPython** to your ESP32-S2:
   - Download: [micropython.org/download](https://micropython.org/download/)
   - Use Thonny IDE: *Tools → MicroPython → Install MicroPython*

2. **Install CH340 Driver** (if board not detected):
   - Windows: [WCH Driver](http://www.wch-ic.com/downloads/CH341SER_EXE.html)
   - Mac/Linux: Usually pre-installed

3. **Connect to Thonny**:
   - Interpreter: `MicroPython (ESP32)`
   - Port: Your COM/USB port

4. **Save `main.py` and `secrets.py`** to the device and run.

---

## ⚙️ Configuration

Edit these values in `secrets.py`:

```python
WIFI_SSID = "your_wifi_name"
WIFI_PASSWORD = "your_wifi_password"

TELEGRAM_TOKEN = "123456789:ABCdefGHIjklADASDASqrsTUVwxyz"  # From @BotFather
TELEGRAM_CHAT_ID = "4234234324321"                          # From @userinfobot

SERVER_URL = "http://your-server:port/endpoint"         # Your monitor target
```

### Get Telegram Credentials:
1. Message **@BotFather** → `/newbot` → get **Token**
2. Message **@userinfobot** → get **Chat ID**
3. Send `/start` to your new bot (so it can message you)

---

## 📡 Usage

```text
Connecting to WiFi...
Connected! IP: 192.168.1.100
Syncing Time...
Time synced: (2026, 3, 10, 14, 30, 0, ...)
Telegram: OK 200

--- VPS HTTP ---
URL: http://85.8.6.29:16954/endpoint
Status Code: 200
>>> SUCCESS <<<
LED ON (2 sec)
```

**LED Behavior**:
| Status | LED |
|--------|-----|
| WiFi fail | Blink 0.5s |
| HTTP 200 | Solid ON 2s |
| HTTP error | Quick blink ×3 |

---

---

## 🔐 Security Notes

- This project uses **HTTP by default** for simplicity. For production:
  - Use HTTPS with valid certificates
  - Store secrets in `secrets.py`
  - Consider adding authentication to your endpoints

---

## 📄 License

MIT License — feel free to use, modify, and share.

---

> 💡 **Tip**: Start with `http://` endpoints to debug, then switch to `https://` once everything works.

**Made with ❤️ for IoT tinkering**
