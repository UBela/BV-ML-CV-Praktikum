import cv2
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter
import threading
import queue

class VideoApp:
    instance = None
    current_frame_class = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = cls(*args, **kwargs)
        return cls.instance

    def __init__(self, window, window_title, video_source=0, width=640, height=480):
        self.window = window
        self.window.title(window_title)
        self.width = width
        self.height = height
        print(self.width, self.height)

        self.vid = cv2.VideoCapture(video_source)
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=1, padx=(20, 0), pady=(20, 0))
        self.image_on_canvas = None

        self.current_frame = None
        self.is_playing = False
        self.queue = queue.Queue(maxsize=10)
        self.thread = threading.Thread(target=self.video_stream, args=())
        self.thread.daemon = True
        self.thread.start()

        self.update()
        self.window.bind("<Key>", self.on_key_press)

    def video_stream(self):
        while True:
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.current_frame = frame.copy()
                VideoApp.current_frame_class = self.current_frame 
                frame = cv2.resize(frame, (self.width, self.height))
                
                try:
                    self.queue.put(frame, True, 0.02)
                except queue.Full:
                    pass

    def update(self):
        try:
            frame = self.queue.get(True, 0.02)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

            if self.image_on_canvas is None:
                self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            else:
                self.canvas.itemconfig(self.image_on_canvas, image=self.photo)
                self.canvas.update()
        except queue.Empty:
            pass

        self.window.after(10, self.update)

    def on_key_press(self, event):
        if event.char == 'q':
            self.window.destroy()

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

camera_ip = "http://192.168.178.68:81/stream"
video_source = camera_ip
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root, "Live Video Feed", video_source)
    root.mainloop()
