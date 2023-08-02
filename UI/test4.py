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
import tkinter
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
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
      def __init__(self):
         super().__init__()
         self.width = 900
         self.height = 600
         self.image_datas_Log = []
         self.image_ids_Log = []
         self.timestamps_Log = []
         self.plate_formats_Log = []
         self.image_datas_Accepted = []
         self.image_ids_Accepted = []
         self.timestamps_Accepted = []
         self.plate_formats_Accepted = []
         self.current_image_index = 0
         self.current_delete_image_index = -1
         self.button_index = 0
         self.button_accepted=[]
         self.button_log=[]
         host = "snuffleupagus.db.elephantsql.com"
         port = "5432"
         database = "lvyoqndm"
         user = "lvyoqndm"
         password = "X8HtTPeJRhM89GYr8s36GrBnp5aOI9P2"
         self.textbox = customtkinter.CTkTextbox(self,width=500,height=200)
         self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0))  
         self.textbox.configure(state="disabled")
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
         self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted = DatabaseManager.retrieve_images_from_database()
         print(self.image_ids_Accepted)
         print(self.timestamps_Accepted)
         print(self.plate_formats_Accepted)
        
         self.title("Praktikum UI")
         self.geometry(f"{1100}x{580}")

         # configure grid layout (4x4)
         self.grid_columnconfigure(1, weight=1)
         self.grid_columnconfigure((2, 3), weight=0)
         self.grid_rowconfigure((0, 1, 2), weight=1)
         #################################################################################
        
         def load_image_data_into_accepted_table(self):
             
                 self.textbox.configure(state="normal") 
                 image_data = self.image_datas_Log[self.current_image_index].tobytes()
                 plate_format = self.plate_formats_Log[self.current_image_index] 
                 query = "SELECT plate_format FROM license_plates_access_accepted WHERE plate_format = %s;"
                 c.execute(query, (plate_format,))
                 result = c.fetchone()
                 if result:
                     print(f"Plate format '{plate_format}' already exists. Skipping image data upload.")
                     self.textbox.insert(END,f"Plate format '{plate_format}' already exists. Skipping image data upload.\n")
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

                     print("Image data loaded into license_plates_access_accepted table.")

                     self.textbox.insert(END,"Image data loaded into accepted table.\n")
                     load_Accepted_current(self,self.current_image_index)
                     print(str(self.current_image_index)+ "wurde hochgeladen" )   
                 self.textbox.configure(state="disabled") 
                 self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted = DatabaseManager.retrieve_images_from_database()
        
        #################################################################################
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
                 print( self.current_delete_image_index)
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
                     print(f"Plate format '{plate_format}' deleted from license_plates_access_accepted table.")
                     self.textbox.insert(END,f"Plate format '{plate_format}' deleted from license_plates_access_accepted table.")
                     self.button_accepted[self.current_delete_image_index].pack_forget()
                     self.button_accepted.pop(self.current_delete_image_index)
                 else:
                     print(f"Plate format '{plate_format}' does not exist in license_plates_access_accepted table. No deletion performed.")
                     self.textbox.insert(END,f"Plate format '{plate_format}' does not exist in license_plates_access_accepted table. No deletion performed.\n")
                 c.close()
                 conn.close()
             except psycopg2.Error as e:
                 print("Error connecting to the database:")
                 self.textbox.insert(END,"Error connecting to the database:\n")
                 print(e)
             print("wurde ausgeführt")
             self.textbox.insert(END,"wurde ausgeführt\n")
             self.textbox.configure(state="disabled")
            
             self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted = DatabaseManager.retrieve_images_from_database()
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
            print("All data deleted from license_plates_access_accepted table.")
            print("wurde ausgeführt")
            self.textbox.insert(END,"All data deleted from license_plates_access_accepted table.\n")
            self.textbox.configure(state="disabled")
            self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted = DatabaseManager.retrieve_images_from_database()  


         # create sidebar frame with widgets
         self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
         self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
         self.sidebar_frame.grid_rowconfigure(4, weight=1)
         self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Kamera UI", font=customtkinter.CTkFont(size=20, weight="bold"))
         self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
         self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="Delete", command= lambda:delete_plate_from_database(self))
         self.sidebar_button_3= customtkinter.CTkButton(self.sidebar_frame,text="Delete All", command= lambda:delete_plates_all_from_database(self))
         print(self.sidebar_button_1.cget("fg_color"))
         if(self.current_delete_image_index == -1):
            self.sidebar_button_1.configure(fg_color="grey",hover="false")
         self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
         self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
         self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text="Allow Access",command=lambda:load_image_data_into_accepted_table(self))#command=load_image_data_into_accepted_table(self)
         self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
         self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
         self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
         self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                    command=self.change_appearance_mode_event)
         self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
         self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
         self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
         self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                            command=self.change_scaling_event)
         self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

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
        
         image = Image.open("C:/Users/raoul/Downloads/BV-ML-CV-Praktikum/TestImagesSet1/image_1.jpg")
         # Convert the original image to PhotoImage using ImageTk
         #photo = ImageTk.PhotoImage(image_with_rounded_edges)
         self.bg_image = customtkinter.CTkImage(apply_rounded_edges(image),
                                            size=(self.width*0.4, self.height*0.4))
        
         #label on image 
         self.bg_image_label = customtkinter.CTkLabel(self,text="", image=self.bg_image)
         self.bg_image_label.grid(row=0, column=1)
        
         
         def display_image(self):
             photo = self.image_datas_Log[self.current_image_index]
             self.bg_image = customtkinter.CTkImage(apply_rounded_edges(photo,8), size=(self.width*0.4, self.height*0.4))
             self.bg_image_label = customtkinter.CTkLabel(self,text="", image=self.bg_image)
             self.bg_image_label.configure(image=self.bg_image)
             self.bg_image_label.grid(row=0, column=1)
             #photo.show()    

         def change_delete_index(index):
             print("Before:", self.current_delete_image_index)
             self.current_delete_image_index=index
             print("After:", self.current_delete_image_index)
             if(self.current_delete_image_index != -1): 
                self.sidebar_button_1.configure(fg_color=['#3a7ebf', '#1f538d'],hover="true")
            
         def change_image(index):
             self.current_delete_image_index = -1
             self.current_image_index = index
             if(self.current_delete_image_index == -1): 
                self.sidebar_button_1.configure(fg_color="grey",hover="false")
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
                print(str(self.button_accepted[0]))
                if(self.load_info):
                    self.textbox.configure(state="normal")   
                    self.textbox.insert(END, str(self.plate_formats_Accepted[i])+"has been added.\n")  
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
                
                self.button_log.append( customtkinter.CTkButton(master=self.scrollable_frame,
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
            plate_format = self.plate_formats_Log[index]

            # Füge den Button mit dem aktuellen Kennzeichen zum Pack hinzu
            plate_text = f"{self.timestamps_Log[self.current_image_index]} | {plate_format} | ACCESS"
            self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted = DatabaseManager.retrieve_images_from_database()
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

            # Füge den Button mit dem aktuellen Kennzeichen zum Pack hinzu
            plate_text = f"{self.timestamps_Log[self.current_image_index]} | {plate_format} | ACCESS"
            self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted = DatabaseManager.retrieve_images_from_database()
            # Anzahl der bereits akzeptierten Buttons
            current_Log_index = len(self.button_log)
            
            # Lambda-Funktion, die self.current_delete_image_index auf den aktuellen Index setzt
            set_delete_index_command = lambda idx=current_accepted_index: change_delete_index(idx)

            self.button_log.append( customtkinter.CTkButton(master=self.scrollable_frame,
                                    width= 550,corner_radius=0,height=40 ,
                                    text=str(self.timestamps_Log[current_Log_index])+ " | " + str(self.plate_formats_Log[current_Log_index])+ " | " + "NO ACCESS",border_width=1,
                                    command=set_delete_index_command))
            self.button_log[-1].pack()
  
        
         def write_text_entry():
                self.textbox.configure(state="normal") 
                license_plate = self.entry.get()  
                
                if(license_plate!=""):
                   if(is_valid_license_plate(license_plate)):
                      self.textbox.insert(END,"Das eingegebene Kennzeichen %s ist gültig.\n" % (license_plate))
                   else: 
                      self.textbox.insert(END,"Das eingegebene Kennzeichen %s ist ungültig.\n" % (license_plate))
                self.textbox.configure(state="disabled")
                start = self.textbox.index("end-1c linestart")
                end = self.textbox.index("end-1c lineend")
                self.textbox.tag_add("gray_bg", start, end)
                self.textbox.configure("gray_bg", bg="gray", padx=1, pady=1)
                


         def is_valid_license_plate(license_plate):
            # Definiere das erwartete Kennzeichenmuster: XX-1234
            pattern = pattern = r'^[A-Z]{1,3}[-]?[A-Z]{1,2}\d{1,4}$'

            # Überprüfe, ob das eingegebene Kennzeichen dem Muster entspricht
            if re.match(pattern, license_plate):
                return True
            else:
                return False
          

         def upload_image_to_database(cursor, image_path, is_allowed, license_plate):
            try:
                # Bild in die Datenbank laden
                image_data = open(image_path, 'rb').read()

                # Aktuelles Datum und Uhrzeit als Timestamp erhalten
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

                # Bild in die Datenbank laden und Timestamp sowie license_plate und is_allowed hinzufügen
                cursor.execute("""
                    INSERT INTO license_plates_access_log (image_data, timestamp, plate_format, is_allowed) 
                    VALUES (%s, %s, %s, %s);
                """, (psycopg2.Binary(image_data), timestamp, license_plate, is_allowed))
                cursor.connection.commit()

                print(f"Datei '{os.path.basename(image_path)}' erfolgreich hochgeladen.")
                print(f"License Plate: {license_plate}, Zugelassen: {is_allowed}")
            except psycopg2.Error as e:
                print(f"Fehler beim Hochladen der Datei '{os.path.basename(image_path)}': {e}")
            self.image_datas_Log,self.image_ids_Log,self.timestamps_Log,self.plate_formats_Log,self.image_ids_Accepted,self.timestamps_Accepted,self.plate_formats_Accepted = DatabaseManager.retrieve_images_from_database()
            load_Accepted_current(self,self.current_image_index)

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

                   
