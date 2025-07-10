# Helmet Detection System

This project is a real-time helmet detection system using YOLOv8. It processes multiple RTSP camera streams and activates an alarm (via USB or ESP32 over Wi-Fi) when a person is detected **not wearing a helmet**.

---

## 📁 Project Structure

Helmet_Detection_IP/
│
├── multi_camera_main.py              # Main runner file
├── gui.py               # Tkinter GUI to manage cameras
├── detector.py          # YOLO model loader and prediction logic
├── camera_worker.py     # RTSP camera stream capture using threads
├── alarm.py             # USB and Wi-Fi communication with buzzer (ESP32)
├── config.yaml          # Configuration file for model and camera settings
├── requirements.txt     # Python package dependencies

## 🔧 Setup Instructions
1. Clone the Repository

'''git clone https://github.com/your-repo/helmet-detection.git
cd helmet-detection'''

