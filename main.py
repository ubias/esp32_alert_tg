import network
import urequests
import time
import ntptime  # For syncing time (required for HTTPS)
from machine import Pin
import secrets

# --- CONFIGURATION ---
WIFI_SSID = secrets.WIFI_SSID
WIFI_PASSWORD = secrets.WIFI_PASSWORD
#
servers = secrets.servers

# ---------------------

# Telegram Config
TELEGRAM_TOKEN = secrets.TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = secrets.TELEGRAM_CHAT_ID

# LED Pin 
LED_PIN = 15 
# ---------------------
# Setup LED
led = Pin(LED_PIN, Pin.OUT)
led.off()
# ---------------------

def connect_wifi(ssid, psw):
    print("Connecting to WiFi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psw)
    
    # Wait for connection (max 10 seconds)
    timeout = 10
    while not wlan.isconnected() and timeout > 0:  
        print(".", end="")
        time.sleep(1)
        timeout -= 1
        
    if wlan.isconnected():  
        print("\nConnected! IP:", wlan.ifconfig()[0])
        return True
    else:
        print("\nFailed to connect. Check password.")
        return False

def sync_time() :
    print("Syncing Time (Required for HTTPS)...")
    try:
        ntptime.settime()
        t = time.localtime()
        fr_t = "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format( t[2], t[1], t[0], (t[3]+3), t[4], t[5])
        return str(fr_t)
    except Exception as e:
        print("Time sync failed:", e)

def send_telegram_message(message):
    try:
        gc.collect()
        
        # USE GET INSTEAD OF POST (simpler, less memory)
        # URL encode the message (replace spaces with %20, etc.)
        safe_message = message.replace(' ', '%20').replace('!', '%21')
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={safe_message}"
        
        print("Sending Telegram (GET)...")
        # print("Free memory:", gc.mem_free())
        
        # Simple GET request (no headers, no body)
        response = urequests.get(url)
        
        print("Telegram Status:", response.status_code)
        
        if response.status_code == 200:
            print(">>> Telegram Sent! <<<")
            result = True
        else:
            print(">>> Telegram Failed! <<<")
            result = False
            
        response.close()
        gc.collect()
        return result
        
    except Exception as e:
        print("Telegram Error:", e)
        return False


def http_ping_pong_d(server: str):
    led.off() 
    try:
        print("\n--- Sending HTTP Requests ---")
        response = urequests.get(server)
        status = response.status_code
        print(f"For VPS {server} Status Code:", status)
            
        if status == 200:
            result = True
        else:
            result = False
        
        response.close()
        return result
            
    except Exception as e:
        print("Request failed:", e)
        return False

# --- MAIN ---
if connect_wifi(WIFI_SSID, WIFI_PASSWORD):
    count_t = 0
    msg_t = sync_time()  # Sync time before making HTTPS requests
    
    # Send a startup message
    send_telegram_message(f"ESP32 is started! TIME: {msg_t}")

    while True:
        # http_ping_pong()
        for name, address in servers.items():
            if not http_ping_pong_d(address):         
                # Send Alert
                print("Trying tg msg...") 
                send_telegram_message(f"ESP32_Ping_BAD_Status_For VPS {name}")

        time.sleep(1800) # Wait 30 minutes (Don't spam Telegram!)
        if count_t > 48:
            count_t = 0
            send_telegram_message(f"ESP32_Just_Working...")
        count_t = count_t + 1 # one time a day send check msg
else:
    print("WiFi Failed. Blinking LED.")
    while True:
        led.on(); time.sleep(0.5); led.off(); time.sleep(0.5)
        time.sleep(300)
        connect_wifi(WIFI_SSID, WIFI_PASSWORD)
