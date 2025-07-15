# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from tkinter.scrolledtext import ScrolledText
# import yaml
# import subprocess
# import threading
# import re
# import os

# CONFIG_PATH = "config.yaml"
# ESP_FILE_PATH = "ESP/ESP.ino"
# LOGO_PATH = "Axis_log.png"


# class HelmetGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Helmet Detection Control Panel")

#         self.load_config()
#         self.setup_ui()

#     def load_config(self):
#         with open(CONFIG_PATH, 'r') as f:
#             self.config = yaml.safe_load(f)

#     def save_config(self):
#         with open(CONFIG_PATH, 'w') as f:
#             yaml.dump(self.config, f)

#     def setup_ui(self):
#         top_frame = tk.Frame(self.root)
#         top_frame.pack(anchor="nw")

#         logo_img = tk.PhotoImage(
#             file=LOGO_PATH).subsample(6, 6)  # Smaller logo
#         logo_label = tk.Label(top_frame, image=logo_img, anchor="nw")
#         logo_label.image = logo_img
#         logo_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

#         # ==== Camera Input Fields ====
#         self.camera_entries = []
#         cam_frame = tk.LabelFrame(self.root, text="Camera URLs")
#         cam_frame.pack(fill="x", padx=10, pady=5)

#         for i in range(4):
#             frame = tk.Frame(cam_frame)
#             frame.pack(fill="x", pady=2)
#             tk.Label(frame, text=f"Camera {i}:").pack(side="left")
#             entry = tk.Entry(frame, width=80)
#             entry.pack(side="left", padx=5)
#             if i < len(self.config['camera_feeds']):
#                 entry.insert(0, self.config['camera_feeds'][i])
#             self.camera_entries.append(entry)

#         btn_frame = tk.Frame(cam_frame)
#         btn_frame.pack(pady=5)
#         tk.Button(btn_frame, text="Update Cameras",
#                   command=self.update_camera_feeds).pack()

#         # ==== ESP Settings ====
#         esp_frame = tk.LabelFrame(self.root, text="ESP Settings")
#         esp_frame.pack(fill="x", padx=10, pady=5)

#         tk.Label(esp_frame, text="ESP IP:").pack(side="left", padx=5)
#         self.esp_ip_entry = tk.Entry(esp_frame, width=20)
#         self.esp_ip_entry.pack(side="left")
#         self.esp_ip_entry.insert(0, self.config.get('esp_ip', ''))

#         self.use_wifi_var = tk.BooleanVar(
#             value=self.config.get('use_wifi', False))
#         tk.Checkbutton(esp_frame, text="Use WiFi",
#                        variable=self.use_wifi_var).pack(side="left", padx=10)

#         tk.Label(esp_frame, text="Serial Port:").pack(side="left", padx=5)
#         self.serial_port_entry = tk.Entry(esp_frame, width=20)
#         self.serial_port_entry.pack(side="left")
#         try:
#             with open("alarm.py", "r") as f:
#                 alarm_code = f.read()
#             match = re.search(r'SERIAL_PORT\s*=\s*"(.*?)"', alarm_code)
#             if match:
#                 self.serial_port_entry.insert(0, match.group(1))
#         except:
#             pass

#         tk.Button(esp_frame, text="WiFi Settings",
#                   command=self.open_wifi_settings).pack(side="left", padx=10)
#         tk.Button(esp_frame, text="Update ESP Config",
#                   command=self.update_esp_config).pack(side="left", padx=10)

#         # ==== Run Button ====
#         tk.Button(self.root, text="RUN", command=self.run_script,
#                   height=2, width=15, bg='green', fg='white').pack(pady=10)

#         # ==== Logs ====
#         log_frame = tk.LabelFrame(self.root, text="Logs")
#         log_frame.pack(fill="both", expand=True, padx=10, pady=5)

#         self.log_output = ScrolledText(log_frame, height=10)
#         self.log_output.pack(fill="both", expand=True)

#     def update_camera_feeds(self):
#         self.config['camera_feeds'] = [e.get()
#                                        for e in self.camera_entries if e.get().strip() != '']
#         self.save_config()
#         messagebox.showinfo("Saved", "Camera feeds updated in config.yaml")

#     def update_esp_config(self):
#         self.config['esp_ip'] = self.esp_ip_entry.get().strip()
#         self.config['use_wifi'] = self.use_wifi_var.get()
#         self.save_config()

#         serial_port = self.serial_port_entry.get().strip()
#         if serial_port:
#             try:
#                 with open("alarm.py", 'r') as f:
#                     code = f.read()
#                 code = re.sub(r'SERIAL_PORT\s*=\s*".*?"',
#                               f'SERIAL_PORT = "{serial_port}"', code)
#                 with open("alarm.py", 'w') as f:
#                     f.write(code)
#             except Exception as e:
#                 messagebox.showerror(
#                     "Error", f"Failed to update alarm.py: {e}")
#                 return

#         messagebox.showinfo("Saved", "ESP and Serial config updated")

#     def open_wifi_settings(self):
#         win = tk.Toplevel(self.root)
#         win.title("WiFi Settings")

#         tk.Label(win, text="SSID:").grid(row=0, column=0, padx=10, pady=5)
#         ssid_entry = tk.Entry(win, width=30)
#         ssid_entry.grid(row=0, column=1)

#         tk.Label(win, text="Password:").grid(row=1, column=0, padx=10, pady=5)
#         pass_entry = tk.Entry(win, width=30)
#         pass_entry.grid(row=1, column=1)

#         def save_wifi():
#             ssid = ssid_entry.get().strip()
#             pwd = pass_entry.get().strip()
#             if ssid and pwd:
#                 with open(ESP_FILE_PATH, 'r') as f:
#                     code = f.read()
#                 code = re.sub(r'const char\* ssid = ".*?";',
#                               f'const char* ssid = "{ssid}";', code)
#                 code = re.sub(r'const char\* password = ".*?";',
#                               f'const char* password = "{pwd}";', code)
#                 with open(ESP_FILE_PATH, 'w') as f:
#                     f.write(code)
#                 messagebox.showinfo(
#                     "Saved", "WiFi credentials updated in ESP.ino")
#                 win.destroy()

#         tk.Button(win, text="Save", command=save_wifi).grid(
#             row=2, column=0, columnspan=2, pady=10)

#     def run_script(self):
#         def runner():
#             process = subprocess.Popen(
#                 ["python3", "multi_camera_main.py"],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.STDOUT,
#                 text=True
#             )
#             for line in process.stdout:
#                 self.log_output.insert(tk.END, line)
#                 self.log_output.see(tk.END)
#         threading.Thread(target=runner, daemon=True).start()


# if __name__ == '__main__':
#     root = tk.Tk()
#     app = HelmetGUI(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import yaml
import subprocess
import threading
import re
import os

CONFIG_PATH = "config.yaml"
ESP_FILE_PATH = "ESP/ESP.ino"
LOGO_PATH = "Axis_log.png"


class HelmetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Helmet Detection Control Panel")

        self.load_config()
        self.setup_ui()

    def load_config(self):
        with open(CONFIG_PATH, 'r') as f:
            self.config = yaml.safe_load(f)

    def save_config(self):
        with open(CONFIG_PATH, 'w') as f:
            yaml.dump(self.config, f)

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(anchor="nw")

        logo_img = tk.PhotoImage(file=LOGO_PATH).subsample(6, 6)
        logo_label = tk.Label(top_frame, image=logo_img, anchor="nw")
        logo_label.image = logo_img
        logo_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # ==== Camera Input Fields ====
        self.camera_entries = []
        self.title_entries = []

        cam_frame = tk.LabelFrame(self.root, text="Camera URLs")
        cam_frame.pack(fill="x", padx=10, pady=5)

        for i in range(4):
            frame = tk.Frame(cam_frame)
            frame.pack(fill="x", pady=2)
            tk.Label(frame, text=f"Camera {i}:").pack(side="left")

            url_entry = tk.Entry(frame, width=60)
            url_entry.pack(side="left", padx=5)
            if i < len(self.config.get('camera_feeds', [])):
                url_entry.insert(0, self.config['camera_feeds'][i])
            self.camera_entries.append(url_entry)

            title_entry = tk.Entry(frame, width=20)
            title_entry.pack(side="left", padx=5)
            if i < len(self.config.get('camera_titles', [])):
                title_entry.insert(0, self.config['camera_titles'][i])
            self.title_entries.append(title_entry)

        btn_frame = tk.Frame(cam_frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Update Cameras",
                  command=self.update_camera_feeds).pack()

        # ==== ESP Settings ====
        esp_frame = tk.LabelFrame(self.root, text="ESP Settings")
        esp_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(esp_frame, text="ESP IP:").pack(side="left", padx=5)
        self.esp_ip_entry = tk.Entry(esp_frame, width=20)
        self.esp_ip_entry.pack(side="left")
        self.esp_ip_entry.insert(0, self.config.get('esp_ip', ''))

        self.use_wifi_var = tk.BooleanVar(
            value=self.config.get('use_wifi', False))
        tk.Checkbutton(esp_frame, text="Use WiFi",
                       variable=self.use_wifi_var).pack(side="left", padx=10)

        tk.Label(esp_frame, text="Serial Port:").pack(side="left", padx=5)
        self.serial_port_entry = tk.Entry(esp_frame, width=20)
        self.serial_port_entry.pack(side="left")
        try:
            with open("alarm.py", "r") as f:
                alarm_code = f.read()
            match = re.search(r'SERIAL_PORT\s*=\s*"(.*?)"', alarm_code)
            if match:
                self.serial_port_entry.insert(0, match.group(1))
        except:
            pass

        tk.Button(esp_frame, text="WiFi Settings",
                  command=self.open_wifi_settings).pack(side="left", padx=10)
        tk.Button(esp_frame, text="Update ESP Config",
                  command=self.update_esp_config).pack(side="left", padx=10)

        # ==== Run Button ====
        tk.Button(self.root, text="RUN", command=self.run_script,
                  height=2, width=15, bg='green', fg='white').pack(pady=10)

        # ==== Logs ====
        log_frame = tk.LabelFrame(self.root, text="Logs")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_output = ScrolledText(log_frame, height=10)
        self.log_output.pack(fill="both", expand=True)

    def update_camera_feeds(self):
        self.config['camera_feeds'] = [e.get().strip()
                                       for e in self.camera_entries if e.get().strip()]
        self.config['camera_titles'] = [t.get().strip()
                                        for t in self.title_entries][:len(self.config['camera_feeds'])]
        self.save_config()
        messagebox.showinfo(
            "Saved", "Camera feeds and titles updated in config.yaml")

    def update_esp_config(self):
        self.config['esp_ip'] = self.esp_ip_entry.get().strip()
        self.config['use_wifi'] = self.use_wifi_var.get()
        self.save_config()

        serial_port = self.serial_port_entry.get().strip()
        if serial_port:
            try:
                with open("alarm.py", 'r') as f:
                    code = f.read()
                code = re.sub(r'SERIAL_PORT\s*=\s*".*?"',
                              f'SERIAL_PORT = "{serial_port}"', code)
                with open("alarm.py", 'w') as f:
                    f.write(code)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to update alarm.py: {e}")
                return

        messagebox.showinfo("Saved", "ESP and Serial config updated")

    def open_wifi_settings(self):
        win = tk.Toplevel(self.root)
        win.title("WiFi Settings")

        tk.Label(win, text="SSID:").grid(row=0, column=0, padx=10, pady=5)
        ssid_entry = tk.Entry(win, width=30)
        ssid_entry.grid(row=0, column=1)

        tk.Label(win, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        pass_entry = tk.Entry(win, width=30)
        pass_entry.grid(row=1, column=1)

        def save_wifi():
            ssid = ssid_entry.get().strip()
            pwd = pass_entry.get().strip()
            if ssid and pwd:
                with open(ESP_FILE_PATH, 'r') as f:
                    code = f.read()
                code = re.sub(r'const char\* ssid = ".*?";',
                              f'const char* ssid = "{ssid}";', code)
                code = re.sub(r'const char\* password = ".*?";',
                              f'const char* password = "{pwd}";', code)
                with open(ESP_FILE_PATH, 'w') as f:
                    f.write(code)
                messagebox.showinfo(
                    "Saved", "WiFi credentials updated in ESP.ino")
                win.destroy()

        tk.Button(win, text="Save", command=save_wifi).grid(
            row=2, column=0, columnspan=2, pady=10)

    def run_script(self):
        def runner():
            process = subprocess.Popen(
                ["python3", "multi_camera_main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in process.stdout:
                self.log_output.insert(tk.END, line)
                self.log_output.see(tk.END)
        threading.Thread(target=runner, daemon=True).start()


if __name__ == '__main__':
    root = tk.Tk()
    app = HelmetGUI(root)
    root.mainloop()
