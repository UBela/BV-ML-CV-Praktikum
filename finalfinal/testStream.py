import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import queue

url = 'http://192.168.178.68:81/stream'  # Replace with your ESP32-CAM IP

class App:
    def __init__(self, window, window_title, video_source=url):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = tk.Button(window, text="Snapshot", width=10, command=self.snapshot)
        self.btn_snapshot.pack(pady=20)

        # Thread-safe queue for frames
        self.queue = queue.Queue()
        
        # Start frame-fetching thread
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.fetch_frames)
        self.thread.start()

        self.update()
        self.window.mainloop()

    def snapshot(self):
        if not self.queue.empty():
            frame = self.queue.get()
            cv2.imwrite("snapshot.jpg", frame)

    def fetch_frames(self):
        while not self.stop_event.is_set():
            ret, frame = self.vid.read()
            if ret:
                self.queue.put(frame)

    def update(self):
        if not self.queue.empty():
            frame = self.queue.get()
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def __del__(self):
        self.stop_event.set()
        self.thread.join()
        if self.vid.isOpened():
            self.vid.release()

root = tk.Tk()
app = App(root, "Tkinter and OpenCV with Threading")
