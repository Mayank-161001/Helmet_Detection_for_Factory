import threading
import atexit
import yaml
from detector import load_class_names, load_model
from camera_worker import process_camera


def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)
    

def cleanup_all():
    print("[EXIT] Cleaning up resources...")
    try:
        cv2.destroyAllWindows()  # Close OpenCV windows
    except Exception as e:
        print(f"[EXIT] cv2 error: {e}")


def main():
    config = load_config()
    model = load_model(config['model_path'])

    class_names, helmet_class, no_helmet_class = load_class_names(
        config['class_file'])
    feeds = config['camera_feeds']

    use_wifi = config.get('use_wifi', False)
    esp_ip = config.get('esp_ip', None)

    cooldown = config.get('alarm_cooldown_sec', 5)

    threads = []
    for cam_id, stream_url in enumerate(feeds):
        t = threading.Thread(target=process_camera, args=(
            cam_id,
            stream_url,
            model,
            config['confidence_threshold'],
            helmet_class,
            no_helmet_class,
            cooldown,
            use_wifi,
            esp_ip
        ))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
