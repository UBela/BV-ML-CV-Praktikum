def __init__(self):
    # ... other initialization code ...
    self.host = "snuffleupagus.db.elephantsql.com"
    self.port = "5432"
    self.database = "lvyoqndm"
    self.user = "lvyoqndm"
    self.password = "X8HtTPeJRhM89GYr8s36GrBnp5aOI9P2"
    try:
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
    except psycopg2.Error as e:
                 print("Error connecting to the database:")
                 print(e) 
import numpy as np   
import tkinter as tk
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk, ImageDraw, ImageOps
import os
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
import psycopg2
from io import BytesIO
from DatabaseManager import DatabaseManager
import re
import cv2
from live_stream import VideoApp
import time
import find_license_plate_id as numberplate
import matching as shape
import pickle
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

host = "snuffleupagus.db.elephantsql.com"
port = "5432"
database = "lvyoqndm"
user = "lvyoqndm"
password = "X8HtTPeJRhM89GYr8s36GrBnp5aOI9P2"
try:
    conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
             )
except psycopg2.Error as e:
                 print("Error connecting to the database:")
                 print(e)
c = conn.cursor()
class App(customtkinter.CTk):
      
      def upload_image_to_database(image_path, is_allowed, license_plate):
            # Verbindung zur Datenbank herstellen
   
            print("funktion wird ausgeführt")
            with open(image_path, 'rb') as file:
                image_data = file.read()

            # Aktuelles Datum und Uhrzeit als Timestamp erhalten
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Bild in die Datenbank laden und Timestamp sowie license_plate und is_allowed hinzufügen
            
            c.execute("""
                INSERT INTO license_plates_access_log (image_data, timestamp, plate_format, is_allowed) VALUES (%s, %s, %s, %s);
            """, (psycopg2.Binary(image_data), timestamp, license_plate, is_allowed))
            conn.commit()

            #print(f"Datei '{os.path.basename(image_path)}' erfolgreich hochgeladen.")
            #print(f"License Plate: {license_plate}, Zugelassen: {is_allowed}")
      def __init__(self):
         super().__init__()
         self.width = 900
         self.height = 600
         self.image_datas_Log = []
         self.image_ids_Log = []
         self.timestamps_Log = []
         self.plate_formats_Log = []
         self.plate_access_Log=[]
         self.image_datas_Accepted = []
         self.image_ids_Accepted = []
         self.timestamps_Accepted = []
         self.plate_formats_Accepted = []
         self.current_image_index = -1
         self.current_delete_image_index = -1
         self.button_index = 0
         self.button_accepted=[]
         self.button_log=[]
         self.plate_formats_contour=[]
         self.image_datas_contour=[]

         
         self.textbox = customtkinter.CTkTextbox(self,width=500,height=200)
         self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0))  
         self.textbox.configure(state="disabled")
         
         self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted,self.plate_formats_contour,self.image_datas_contour,self.plate_access_Log  = DatabaseManager.retrieve_images_from_database()
         #print(self.image_ids_Accepted)
         #print(self.timestamps_Accepted)
         #print(self.plate_formats_Accepted)
        
         self.title("Praktikum UI")
         self.geometry(f"{1100}x{580}")

         # configure grid layout (4x4)
         self.grid_columnconfigure(1, weight=1)
         self.grid_columnconfigure((2, 3), weight=0)
         self.grid_rowconfigure((0, 1, 2), weight=1)
         #################################################################################
        
         def load_image_data_into_accepted_table(self):
            if(self.current_image_index != -1):
                 self.textbox.configure(state="normal") 
                 image_data = self.image_datas_Log[self.current_image_index].tobytes()
                 plate_format = self.plate_formats_Log[self.current_image_index] 
                 query = "SELECT plate_format FROM license_plates_access_accepted WHERE plate_format = %s;"
                 c.execute(query, (plate_format,))
                 result = c.fetchone()
                 if result:
                     self.textbox.insert(END,f"Plate format '{plate_format}' already exists. Skipping image data upload.\n"
                                         + "_______________________________________________________\n\n")
                 else:
                    
                    
                     # Retrieve the plate_format from the license_plates_access_log table for the current image_id
                     query = "SELECT plate_format FROM license_plates_access_accepted WHERE id = %s;"
                
                     label = "Accepted"  # Example label value, you can change this accordingly
                     timestamp = datetime.now().replace(microsecond=0)  # Example timestamp value, you can change this accordingly

                     query = """
                     INSERT INTO license_plates_access_accepted (image_data, label, timestamp, plate_format)
                     VALUES (%s, %s, %s, %s);
                     """
                     c.execute(query, ( psycopg2.Binary(image_data), label, timestamp, plate_format))
                     conn.commit()

                     self.textbox.insert(END,f"'{plate_format}' loaded into accepted table.\n"
                                         + "_______________________________________________________\n\n")
                     load_Accepted_current(self,self.current_image_index)
                     print(str(self.current_image_index) + "wurde hochgeladen" )   
                 self.textbox.configure(state="disabled") 
                 self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted,self.plate_formats_contour,self.image_datas_contour,self.plate_access_Log  = DatabaseManager.retrieve_images_from_database()
                 self.current_image_index = -1
        #################################################################################

         def load_image_data_into_accepted_table(self,plate):
                 self.textbox.configure(state="normal") 
                 query = "SELECT plate_format FROM license_plates_access_accepted WHERE plate_format = %s;"
                 c.execute(query, (plate,))
                 result = c.fetchone()
                 if result:
                     self.textbox.insert(END,f"Plate format '{plate}' already exists. Skipping image data upload.\n"
                                         + "_______________________________________________________\n\n")
                 else:
                    
                    
                     # Retrieve the plate_format from the license_plates_access_log table for the current image_id
                     query = "SELECT plate_format FROM license_plates_access_accepted WHERE id = %s;"
                
                     timestamp = datetime.now().replace(microsecond=0)  # Example timestamp value, you can change this accordingly

                     query = """
                     INSERT INTO license_plates_access_accepted ( timestamp, plate_format)
                     VALUES ( %s, %s);
                     """
                     c.execute(query, (  timestamp,plate))
                     conn.commit()

                     self.textbox.insert(END,f"'{plate}' loaded into accepted table.\n"
                                         + "_______________________________________________________\n\n")
                     load_Accepted_current(self,self.current_image_index)
                     print(str(self.current_image_index) + "wurde hochgeladen" )   
                 self.textbox.configure(state="disabled") 
                 self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted,self.plate_formats_contour,self.image_datas_contour,self.plate_access_Log  = DatabaseManager.retrieve_images_from_database()
                 self.current_image_index = -1


         def delete_plate_from_database(self):
             try:
                 conn = psycopg2.connect(
                     host="snuffleupagus.db.elephantsql.com",
                     port="5432",
                     database="lvyoqndm",
                     user="lvyoqndm",
                     password="X8HtTPeJRhM89GYr8s36GrBnp5aOI9P2"
                 )
                 self.textbox.configure(state="normal") 
                 c = conn.cursor()
                 plate_format = self.plate_formats_Accepted[self.current_delete_image_index] 
                 # Check if the plate_format exists in the license_plates_access_accepted table
                 query = "SELECT plate_format FROM license_plates_access_accepted WHERE plate_format = %s;"
                 c.execute(query, (plate_format,))
                 result = c.fetchone()
                 
                 if result and self.current_delete_image_index != -1:
                     # Delete the plate_format from the license_plates_access_accepted table
                     delete_query = "DELETE FROM license_plates_access_accepted WHERE plate_format = %s;"
                     c.execute(delete_query, (plate_format,))
                     conn.commit()
                     
                     self.textbox.insert(END,f"Plate format '{plate_format}' deleted from license_plates_access_accepted table.\n"
                                         + "_______________________________________________________\n\n")
                     self.button_accepted[self.current_delete_image_index].pack_forget()
                     self.button_accepted.pop(self.current_delete_image_index)
                 else:
            
                     self.textbox.insert(END,f"Plate format '{plate_format}' does not exist in license_plates_access_accepted table. No deletion performed.\n"
                                         + "_______________________________________________________\n\n")
                 c.close()
                 conn.close()
             except psycopg2.Error as e:
                 print("Error connecting to the database:")
                 self.textbox.insert(END,"Error connecting to the database:\n"
                                     + "_______________________________________________________\n\n")
             
             self.textbox.configure(state="disabled")
            
             self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted,self.plate_formats_contour,self.image_datas_contour,self.plate_access_Log  = DatabaseManager.retrieve_images_from_database()
         #################################################################################
         def delete_plates_all_from_database(self):      
            # Delete all data from the license_plates_access_accepted table
            delete_query = "DELETE FROM license_plates_access_accepted;"
            c.execute(delete_query)
            conn.commit()

            self.textbox.configure(state="normal") 
            for i, image_id in enumerate(self.plate_formats_Accepted):
                if self.button_accepted[i].winfo_exists():
                   self.button_accepted[i].pack_forget()
            self.textbox.insert(END,"All data deleted from accepted table.\n"
                                + "_______________________________________________________\n\n")
            self.textbox.configure(state="disabled")
            self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted,self.plate_formats_contour,self.image_datas_contour,self.plate_access_Log  = DatabaseManager.retrieve_images_from_database()  


         # create sidebar frame with widgets
         self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
         self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
         self.sidebar_frame.grid_rowconfigure(4, weight=1)
         self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Kamera UI", font=customtkinter.CTkFont(size=20, weight="bold"))
         self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
         self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="Delete", command= lambda:delete_plate_from_database(self))
         self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text="Allow Access",command=lambda:load_image_data_into_accepted_table(self))#command=load_image_data_into_accepted_table(self)
         self.sidebar_button_3= customtkinter.CTkButton(self.sidebar_frame,text="Delete All", command= lambda:delete_plates_all_from_database(self))
         self.sidebar_button_4= customtkinter.CTkButton(self.sidebar_frame,text="Live Feed", command= lambda:start_video(self))
         self.sidebar_button_5= customtkinter.CTkButton(self.sidebar_frame,text="Scan", command= lambda:get_current_image(self))
         
        
         if(self.current_delete_image_index == -1):
            self.sidebar_button_1.configure(fg_color="grey",hover="false",state="disabled")
           
         self.sidebar_button_1.grid(padx=20, pady=10)
         self.sidebar_button_2.grid(padx=20, pady=10)
         self.sidebar_button_3.grid(padx=20, pady=10)
         self.sidebar_button_4.grid(padx=20, pady=10)
         self.sidebar_button_5.grid(padx=20, pady=10)
       
         
         if(self.current_image_index== -1):
                self.sidebar_button_2.configure(fg_color="grey",hover="false",state="disabled")  
         self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
         self.appearance_mode_label.grid( padx=20, pady=(10, 0))
         self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=[ "Dark","Light"],
                                                                    command=self.change_appearance_mode_event)
         self.appearance_mode_optionemenu.grid( padx=20, pady=(10, 10))
         self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
         self.scaling_label.grid( padx=20, pady=(10, 0))
         self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                            command=self.change_scaling_event)
         self.scaling_optionemenu.grid( padx=20, pady=(10, 20))

         # create main entry and button
         self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
         self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

         self.main_button_1 = customtkinter.CTkButton(master=self,text="Enter", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command=lambda:write_text_entry())
         self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
         #
         def apply_rounded_edges(image, radius=30):
         # Create a mask with rounded edges
             mask = Image.new("L", image.size, 0)
             draw = ImageDraw.Draw(mask)
             draw.rounded_rectangle((0, 0, image.width, image.height), radius=radius, fill=255)

             # Apply the mask to the image
             image_with_rounded_edges = Image.new("RGBA", image.size)
             image_with_rounded_edges.paste(image, (0, 0), mask=mask)

             return image_with_rounded_edges
        
         image = Image.open("TestImagesSet1\image_1.jpg")
         # Convert the original image to PhotoImage using ImageTk
         #photo = ImageTk.PhotoImage(image_with_rounded_edges)
         self.bg_image = customtkinter.CTkImage(apply_rounded_edges(image),
                                            size=(self.width*0.4, self.height*0.4))
        
         #label on image 
         self.bg_image_label = customtkinter.CTkLabel(self,text="", image=self.bg_image)
         self.bg_image_label.grid(row=0, column=1,padx=(20, 0), pady=(20, 0))
        
         
         def display_image(self):
             photo = self.image_datas_Log[self.current_image_index]
             self.bg_image = customtkinter.CTkImage(apply_rounded_edges(photo,8), size=(self.width*0.4, self.height*0.4))
             self.bg_image_label = customtkinter.CTkLabel(self,text="", image=self.bg_image)
             self.bg_image_label.configure(image=self.bg_image)
             self.bg_image_label.grid(row=0, column=1,padx=(20, 0), pady=(20, 0))
             #photo.show()   
               
        
         
         camera_ip = "http://192.168.178.68:81/stream"
         #camera_ip = 0

         self.video_app=VideoApp(self,"Live Video Feed", camera_ip)
         def start_video(self):
             if not self.video_app:
                self.canvas = tk.Canvas(self, width=self.width*0.4, height=self.height*0.4)
                self.canvas.grid(row=0, column=1,padx=(20, 0), pady=(20, 0))
                width, height = round(self.width*0.4),round(self.height*0.4)
                self.video_app=VideoApp(self,"Live Video Feed", camera_ip)  
             else:
                 print("Live Video Feed is already active")
                 
    
        ### process for checking 
         def get_current_image(self):

            # delete contents of folder
            dir = "finalfinal/cam_frames"
            if(len(os.listdir(dir)) > 0):
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))

            # save 5 images in folder
            for i in range(5):
                frame = Image.fromarray(self.video_app.current_frame_class)
                frame.save(f"{dir}/frame_{i}.jpg")

            # get numberplate and corresponding image            
            plate, img = numberplate.process_license_plates(dir)
       
            img_for_upload = img.tobytes()
            if (plate == "No License Plate Detected!" or plate == "License Plate Text not Detected!"):
                return
    
            # plate not accepted
            accepted_plates = self.plate_formats_Accepted
            accepted_plates = [plate.replace("-","") for plate in accepted_plates]
            if(plate not in accepted_plates):
                upload_image_to_database_log(img_for_upload, False, license_plate=plate)
                print("not accepted plate")
                return
            # plate accepted and contour exists
            if(plate in self.plate_formats_contour):
                index = self.plate_formats_contour.index(plate)
                contour = self.image_datas_contour[index]
                print(type(contour))
                result = shape.compare_ContourImage(np.asarray(contour), img)
                print("conotur result", result)
                if (not result): # contour doesnt match
                    upload_image_to_database_log(img_for_upload, False, license_plate=plate)
                else:
                    upload_image_to_database_log(img_for_upload, True, license_plate=plate)
            else: # save 
                print("hallo", type(img))
                shape.save_contour(img)
                with open('contour.pkl', 'rb') as f:
                    contour = pickle.load(f)
                upload_image_to_database_log(img_for_upload, True, license_plate=plate)
                upload_image_to_database_contour(contour, plate)
             

        

         def change_delete_index(index):
             print("Before:", self.current_delete_image_index)
             self.current_delete_image_index=index
             self.current_image_index = -1
             print("After:", self.current_delete_image_index)
             if(self.current_delete_image_index != -1): 
                self.sidebar_button_1.configure(fg_color=['#3a7ebf', '#1f538d'],hover="true",state="normal")
             if(self.current_image_index == -1): 
                self.sidebar_button_2.configure(fg_color="grey",hover="false",state="disabled")
            
         def change_image(index):
             self.current_delete_image_index = -1
             self.current_image_index = index
             if(self.current_delete_image_index == -1): 
                self.sidebar_button_1.configure(fg_color="grey",hover="false",state="disabled")
             if(self.current_image_index != -1): 
                self.sidebar_button_2.configure(fg_color=['#3a7ebf', '#1f538d'],hover="true",state="normal")   
             if len(self.image_datas_Log) > 0:
                 display_image(self)

            
                
                
                
         self.scrollable_frame2 = customtkinter.CTkScrollableFrame(self,width=500,height=200, label_text="Accepted LP")
         self.scrollable_frame2.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
         self.load_info =False; 
         def load_Accepted_all(self):
            
            for i, image_id in enumerate(self.plate_formats_Accepted):
                
                self.button_accepted.append(customtkinter.CTkButton(master=self.scrollable_frame2,
                                                width= 550,corner_radius=0,height=40 ,
                                                text=str(self.timestamps_Accepted[i])+ " | " + str(self.plate_formats_Accepted[i])+ " | " + "ACCESS",
                                                border_width=1,
                                                command=lambda index=i : change_delete_index(index)
                                                ))
                
                if(self.load_info):
                    self.textbox.configure(state="normal")   
                    self.textbox.insert(END, str(self.plate_formats_Accepted[i])+"has been added.\n"
                                        + "_______________________________________________________\n\n")  
                    self.textbox.configure(state="disabled")
                self.button_accepted[i].pack()
                
                
                
         load_Accepted_all(self)   
         self.load_info =True;     
            #self.button[0].grid(row=i, column=0, padx=10, pady=(0, 0))
       
         

        
         # create scrollable frame
         self.scrollable_frame = customtkinter.CTkScrollableFrame(self,width=500,height=200, label_text="Access Log")
         self.scrollable_frame.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
         self.scrollable_frame.grid_columnconfigure(0, weight=1)
         self.scrollable_frame_switches = []
         self.scrollable_frame_buttons = []
         # Retrieve images from the database
         
         # Create a Button for each image
         def load_Log(self):
             for i, image_id in enumerate(self.image_ids_Log):
                
                self.button_log.append(customtkinter.CTkButton(master=self.scrollable_frame,
                                                width= 550,corner_radius=0,height=40 ,
                                                text=str(self.timestamps_Log[i])+ " | " + str(self.plate_formats_Log[i])+ " | " + "NO ACCESS",border_width=1,
                                                command=lambda index=i: change_image(index)))
                self.button_log[i].pack()
            
         load_Log(self)
            #   for i, image_id in enumerate(self.image_ids_Log):
            #      button= customtkinter.CTkButton(master=self.scrollable_frame,
            #                                 width= 550,corner_radius=0,height=40 ,
            #                                 text=str(self.timestamps_Log[i])+ " | " + str(self.plate_formats_Log[i])+ " | " + "NO ACCESS",border_width=1,
            #                                 command=lambda index=i: change_image(index))
        
        
         def load_Accepted_current(self, index):        

            # Füge den Button mit dem aktuellen Kennzeichen zum Pack hinzu
            self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted,self.plate_formats_contour,self.image_datas_contour,self.plate_access_Log  = DatabaseManager.retrieve_images_from_database()
            plate_format = self.plate_formats_Accepted[-1]
            plate_text = f"{self.timestamps_Accepted[-1]} | {plate_format} "
            # Anzahl der bereits akzeptierten Buttons
            current_accepted_index = len(self.button_accepted)
            
            # Lambda-Funktion, die self.current_delete_image_index auf den aktuellen Index setzt
            set_delete_index_command = lambda idx=current_accepted_index: change_delete_index(idx)

            self.button_accepted.append(customtkinter.CTkButton(master=self.scrollable_frame2,
                                            width=550, corner_radius=0, height=40,
                                            text=plate_text,
                                            border_width=1,
                                            command=set_delete_index_command
                                            ))
            self.button_accepted[-1].pack()

          
         def load_log_current(self, index):
            plate_format = self.plate_formats_Log[index]
            plate_access=self.plate_access_Log[index]
            # Füge den Button mit dem aktuellen Kennzeichen zum Pack hinzu
            plate_text = f"{self.timestamps_Log[self.current_image_index]} | {plate_format} | {plate_access}"
            self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted,self.plate_formats_contour,self.image_datas_contour,self.plate_access_Log  = DatabaseManager.retrieve_images_from_database()
            # Anzahl der bereits akzeptierten Buttons
            current_Log_index = len(self.button_log)
            
            # Lambda-Funktion, die self.current_delete_image_index auf den aktuellen Index setzt
            set_delete_index_command = lambda idx=self.current_image_index: change_delete_index(idx)
            self.button_log.append(customtkinter.CTkButton(master=self.scrollable_frame,
                                    width= 550,corner_radius=0,height=40 ,
                                    text=plate_text,
                                    border_width=1,
                                    command=set_delete_index_command))
            self.button_log[-1].pack()
  
        
         def write_text_entry():
                self.textbox.configure(state="normal") 
                license_plate = self.entry.get()  
                
                if(license_plate!=""):
                   if(is_valid_license_plate(license_plate)):
                      self.textbox.insert(END,"Das eingegebene Kennzeichen %s ist gültig.\n" % (license_plate)
                                          + "_______________________________________________________\n")
                      load_image_data_into_accepted_table(self,license_plate)
                   else: 
                      self.textbox.insert(END,"Das eingegebene Kennzeichen %s ist ungültig.\n" % (license_plate)
                                          + "_______________________________________________________\n")
                self.textbox.configure(state="disabled")
                start = self.textbox.index("end-1c linestart")
                end = self.textbox.index("end-1c lineend")
                self.textbox.tag_add("gray_bg", start, end)
                self.textbox.configure("gray_bg", padx=1, pady=1)
                


         def is_valid_license_plate(license_plate):
            # Definiere das erwartete Kennzeichenmuster: XX-1234
            pattern = pattern = r'^[A-Z]{1,3}[-]?[A-Z]{1,2}\d{1,4}$'

            # Überprüfe, ob das eingegebene Kennzeichen dem Muster entspricht
            if re.match(pattern, license_plate):
                return True
            else:
                return False
          

         def upload_image_to_database_log(image, is_allowed, license_plate):

           try:
                # Aktuelles Datum und Uhrzeit als Timestamp erhalten
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query="""
                    INSERT INTO license_plates_access_log (image_data, timestamp, plate_format, access) VALUES (%s, %s, %s, %s);
                """
                # Bild in die Datenbank laden und Timestamp sowie license_plate und is_allowed hinzufügen
                c.execute(query, (psycopg2.Binary(image), timestamp, license_plate, is_allowed))
                
                conn.commit()
                print(f"License Plate: {license_plate}, Zugelassen: {is_allowed}")

           except psycopg2.DatabaseError as e:
                # Fehlermeldung ausgeben, wenn ein Datenbankfehler auftritt
                print("Datenbankfehler:", e)
            
           except Exception as e:
                # Allgemeine Fehlermeldung ausgeben
                print("Ein unerwarteter Fehler ist aufgetreten:", e)


         def upload_image_to_database_contour(contour, license_plate):
            
            # Aktuelles Datum und Uhrzeit als Timestamp erhalten
            
            # Bild in die Datenbank laden und Timestamp sowie license_plate und is_allowed hinzufügen
            c.execute("""
                INSERT INTO license_plates_and_images (image_data, plate_format) VALUES ( %s, %s);
            """, (psycopg2.Binary(contour), license_plate))
            conn.commit()
            self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted,self.plate_formats_contour,self.image_datas_contour,self.plate_access_Log  = DatabaseManager.retrieve_images_from_database()

      def open_input_dialog_event(self):
         dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
         print("CTkInputDialog:", dialog.get_input())

      def change_appearance_mode_event(self, new_appearance_mode: str):
         customtkinter.set_appearance_mode(new_appearance_mode)

      def change_scaling_event(self, new_scaling: str):
         new_scaling_float = int(new_scaling.replace("%", "")) / 100
         customtkinter.set_widget_scaling(new_scaling_float)

      def sidebar_button_event(self):
         print("sidebar_button click")
      
   
    # Create an instance of the App class and run the application
if __name__ == "__main__":
  app = App()
  app.mainloop() 
  def close(self):
        self.conn.close()

class VideoApp:
    def __init__(self, window, window_title, video_source=0):
        # ... (other initialization code) ...

        def start_video(self):
            self.is_playing = True
            self.update()

        def stop_video(self):
            self.is_playing = False

        def update(self):
            if self.is_playing:
                ret, frame = self.vid.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                    self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            if self.is_playing:
                # Call update function again after 10 milliseconds (10ms delay)
                self.canvas.after(10, self.update)

        def __del__(self):
            if self.vid.isOpened():
                self.vid.release()
                    
