# Helmet Detection System

This project is a real-time helmet detection system using YOLOv8. It processes multiple RTSP camera streams and activates an alarm (via USB or ESP32 over Wi-Fi) when a person is detected **not wearing a helmet**.

---

## 📁 Project Structure

Helmet_Detection_IP/<br>
│<br>
├── multi_camera_main.py           # Main runner file<br>
├── gui.py               # Tkinter GUI to manage cameras<br>
├── detector.py          # YOLO model loader and prediction logic<br>
├── camera_worker.py     # RTSP camera stream capture using threads<br>
├── alarm.py             # USB and Wi-Fi communication with buzzer (ESP32)<br>
├── config.yaml          # Configuration file for model and camera settings<br>
├── requirements.txt     # Python package dependencies<br>

## 🔧 Setup Instructions

1. Clone the Repository

```javascript 
git clone https://github.com/Mayank-161001/Helmet_Detection_for_Factory.git
```

2. Create and Activate Virtual Environment

3. Install Required Dependencies
```javascript
pip install -r requirements.txt
```
4.🔌 USB Serial Port Detection
```javascript
sudo dmesg | grep tty
```
##✅ To install tkinter on your system :
```javascript
sudo apt-get install python3-tk
```


