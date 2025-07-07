import cv2
import time
import os
from datetime import datetime
from alarm import trigger_alarm
from detector import run_detection


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# def save_violation_images(frame, det, cam_id, frame_index):
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     folder = f"violations/cam{cam_id}"
#     ensure_dir(folder)

#     full_path = f"{folder}/frame{frame_index}_{timestamp}.jpg"
#     crop_path = f"{folder}/cropped_{frame_index}_{timestamp}.jpg"

#     # cv2.imwrite(full_path, frame)

#     x1, y1, x2, y2 = map(int, det['box'])
#     cropped = frame[y1:y2, x1:x2]
#     # cv2.imwrite(crop_path, cropped)


# def log_violation(cam_id, frame_index, violation_rate):
#     ensure_dir("logs")
#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with open("logs/alerts.log", "a") as f:
#         f.write(
#             f"[{now}] Camera {cam_id} | Frame {frame_index} | No helmet | Rate: {violation_rate:.2f}%\n")


# def process_camera(cam_id, stream_url, model, threshold, helmet_class, no_helmet_class, cooldown, use_wifi=False, esp_ip=None):
#     cap = cv2.VideoCapture(stream_url)
#     if not cap.isOpened():
#         print(f"[Camera {cam_id}] ❌ Failed to open stream")
#         return

#     frame_count = 0
#     violations = 0
#     RESIZE_DIM = (800, 750)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print(f"[Camera {cam_id}] Stream ended or failed")
#             break

#         frame_count += 1
#         start = time.time()
#         resized = cv2.resize(frame, RESIZE_DIM)

#         detections = run_detection(model, resized, threshold)

#         violation_detected = False
#         for det in detections:
#             if det['class'] == no_helmet_class:
#                 violations += 1
#                 rate = (violations / frame_count) * 100
#                 trigger_alarm(cam_id, cooldown,
#                               use_wifi=use_wifi, esp_ip=esp_ip)
#                 log_violation(cam_id, frame_count, rate)
#                 # save_violation_images(resized, det, cam_id, frame_count)
#                 violation_detected = True
#                 break

#         for det in detections:
#             x1, y1, x2, y2 = map(int, det['box'])
#             label = f"{det['class']} {det['conf']:.2f}"
#             cv2.rectangle(resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(resized, label, (x1, y1 - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#         fps = 1 / (time.time() - start + 1e-5)
#         stat = f"Cam {cam_id} | FPS: {fps:.2f} | Violations: {violations}"
#         cv2.putText(resized, stat, (10, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

#         cv2.imshow(f'Camera {cam_id}', resized)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyWindow(f'Camera {cam_id}')


#--------------------------------------

# === camera_worker.py ===


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# def save_violation_images(frame, det, cam_id, frame_index):
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     folder = f"violations/cam{cam_id}"
#     ensure_dir(folder)

#     full_path = f"{folder}/frame{frame_index}_{timestamp}.jpg"
#     crop_path = f"{folder}/cropped_{frame_index}_{timestamp}.jpg"

#     cv2.imwrite(full_path, frame)

#     x1, y1, x2, y2 = map(int, det['box'])
#     cropped = frame[y1:y2, x1:x2]
#     cv2.imwrite(crop_path, cropped)


def log_violation(cam_id, frame_index, violation_rate):
    ensure_dir("logs")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/alerts.log", "a") as f:
        f.write(
            f"[{now}] Camera {cam_id} | Frame {frame_index} | No helmet | Rate: {violation_rate:.2f}%\n")


def camera_loop(cam_id, stream_url, model, threshold, helmet_class, no_helmet_class, cooldown, use_wifi, esp_ip, frame_dict, lock):
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print(f"[Camera {cam_id}] ❌ Failed to open stream")
        return

    frame_count = 0
    violations = 0
    RESIZE_DIM = (500, 600)

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"[Camera {cam_id}] Stream ended or failed")
            break

        frame_count += 1
        start = time.time()
        resized = cv2.resize(frame, RESIZE_DIM)

        detections = run_detection(model, resized, threshold)

        violation_detected = False
        for det in detections:
            if det['class'] == no_helmet_class:
                violations += 1
                rate = (violations / frame_count) * 100
                trigger_alarm(cam_id, cooldown,
                              use_wifi=use_wifi, esp_ip=esp_ip)
                log_violation(cam_id, frame_count, rate)
                # save_violation_images(resized, det, cam_id, frame_count)
                violation_detected = True
                break

        for det in detections:
            x1, y1, x2, y2 = map(int, det['box'])
            class_name = det['class']
            label = f"{class_name.upper()} {det['conf']:.2f}"
            color = (0, 255, 0) if class_name == helmet_class else (0, 0, 255)
            cv2.rectangle(resized, (x1, y1), (x2, y2), color, 2)
            cv2.putText(resized, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        fps = 1 / (time.time() - start + 1e-5)
        stat = f"Cam {cam_id} | FPS: {fps:.2f} | Violations: {violations}"
        cv2.putText(resized, stat, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # Store latest frame for GUI thread
        with lock:
            frame_dict[cam_id] = resized

    cap.release()
