import time
import threading
import serial

# Store last time we sent buzz_on
last_sent_time = {}
COOLDOWN = 3  # seconds

# Set your USB serial port and baudrate here
SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    print(f"[USB] Serial connected on {SERIAL_PORT}")
except Exception as e:
    ser = None
    print(f"[USB] Failed to open serial port {SERIAL_PORT}: {e}")


def send_buzzer_command(state, use_wifi, esp_ip=None):
    if use_wifi and esp_ip:
        import requests
        try:
            url = f"http://{esp_ip}/buzz_{'on' if state else 'off'}"
            print(f"[WiFi] Sending request to {url}")
            requests.get(url, timeout=1)
        except Exception as e:
            print(f"[WiFi] Error sending buzzer request: {e}")
    else:
        if ser and ser.is_open:
            cmd = "buzz_on\n" if state else "buzz_off\n"
            try:
                ser.write(cmd.encode())
                print(f"[USB] Sent: {cmd.strip()}")
            except Exception as e:
                print(f"[USB] Error sending serial command: {e}")
        else:
            print("[USB] Serial port not open, can't send command")


def trigger_alarm(camera_id, cooldown, use_wifi=False, esp_ip=None):
    now = time.time()

    if camera_id not in last_sent_time:
        last_sent_time[camera_id] = 0

    # Always try to send 'buzz_on' if cooldown passed
    if now - last_sent_time[camera_id] > COOLDOWN:
        print(f"[ALARM] No helmet detected on Camera {camera_id}")
        threading.Thread(target=send_buzzer_command,
                         args=(True, use_wifi, esp_ip),
                         daemon=True).start()
        last_sent_time[camera_id] = now
