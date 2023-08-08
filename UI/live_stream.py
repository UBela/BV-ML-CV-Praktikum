import cv2
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter
class VideoApp:
    def __init__(self, window, window2, window_title, video_source=0,width=640, height=480):
        self.window = window
        self.window2 = window2
        self.window.title(window_title)
        # Desired dimensions for video stream
        self.width = width
        self.height = height
        print(self.width,self.height)
        # Open video source (use the default camera or a specified video file)
        self.vid = cv2.VideoCapture(video_source)
        
        self.canvas = tk.Canvas(self.window , width=self.width, height=self.height)
        self.canvas.grid(row=0, column=1, padx=(20, 0), pady=(20, 0))
        self.btn_capture = customtkinter.CTkButton(window, text="Capture", command=lambda:get_current_frame(self))
        self.btn_capture.grid(row=1, column=0, padx=(0, 0), pady=(0, 0))
        # Zum Speichern des aktuellen Frames
        self.current_frame = None  
        def get_current_frame(self):
            # Diese Methode gibt das aktuelle Frame zurück.
        # Hier geben wir es einfach aus, aber Sie können es je nach Bedarf weiterverarbeiten.
            if self.current_frame is not None:
               cv2.imshow("Snapshot", self.current_frame)
               cv2.waitKey(0)
               cv2.destroyAllWindows()
        

        self.is_playing = False
        self.start_video()
    def start_video(self):
        self.is_playing = True
        self.update()

    def stop_video(self):
        self.is_playing = False

    def update(self):
        if self.is_playing:
            ret, frame = self.vid.read()
            if ret:
                # Speichere das aktuelle Frame als Klassenattribut
                self.current_frame = frame.copy()
                # livestream
                frame = cv2.resize(frame, (self.width, self.height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        if self.is_playing:
            self.window.after(10, self.update)
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Change the video_source to a specific video file or 0 for the default camera
video_source = 0

root = tk.Tk()
app = VideoApp(root,root,  "Live Video Feed", video_source)
root.mainloop()
