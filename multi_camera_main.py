
# === multi_camera===-------------------------------------------------------------------------------------
import threading
import atexit
import yaml
import cv2
import queue
from detector import load_class_names, load_model
from camera_worker import camera_loop
from alarm import init_serial, close_serial

# Shared dictionary to hold latest frames
frame_dict = {}
lock = threading.Lock()


def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def cleanup_all():
    print("[EXIT] Cleaning up resources...")
    try:
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"[EXIT] cv2 error: {e}")
    close_serial()


def display_frames(camera_titles):
    while True:
        with lock:
            for cam_id, frame in frame_dict.items():
                title = camera_titles[cam_id] if cam_id < len(
                    camera_titles) else f"Camera {cam_id}"
                cv2.imshow(title, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def main():
    init_serial()
    atexit.register(cleanup_all)

    config = load_config()
    model = load_model(config['model_path'])
    class_names, helmet_class, no_helmet_class = load_class_names(
        config['class_file'])

    use_wifi = config.get('use_wifi', False)
    esp_ip = config.get('esp_ip', None)
    cooldown = config.get('alarm_cooldown_sec', 5)

    feeds = config['camera_feeds']
    titles = config.get(
        'camera_titles', [f"Camera {i}" for i in range(len(feeds))])
    threads = []

    for cam_id, stream_url in enumerate(feeds):
        t = threading.Thread(target=camera_loop, args=(
            cam_id, stream_url, model, config['confidence_threshold'],
            helmet_class, no_helmet_class, cooldown, use_wifi, esp_ip,
            frame_dict, lock))
        t.daemon = True
        t.start()
        threads.append(t)

    display_frames(titles)


if __name__ == '__main__':
    main()
