import psycopg2
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
class DatabaseManager:
        image_datas_Log_old=[]
        image_ids_Log_old=[]
        timestamps_Log_old=[]
        plate_formats_Log_old=[]
        image_ids_Accepted_old=[]
        timestamps_Accepted_old=[]
        plate_formats_Accepted_old=[]
        @staticmethod
        def retrieve_images_from_database():
                try:
            # Connect to the PostgreSQL database
                    conn = psycopg2.connect(
                        host="snuffleupagus.db.elephantsql.com",
                        port="5432",
                        database="lvyoqndm",
                        user="lvyoqndm",
                        password="X8HtTPeJRhM89GYr8s36GrBnp5aOI9P2"
                    )
                    c = conn.cursor()
                    query = "SELECT id, image_data, timestamp, plate_format FROM license_plates_access_log;"
                    c.execute(query)
                    results = c.fetchall()
                    image_datas_Log=[]
                    image_ids_Log=[]
                    timestamps_Log=[]
                    plate_formats_Log=[]
                    image_ids_Accepted=[]
                    timestamps_Accepted=[]
                    plate_formats_Accepted=[]
                    for result in results:
                            image_id = result[0]
                            image_data = result[1]
                            timestamp = result[2]
                            plate_format = result[3]
                            try:  
                                # Create an Image object from the binary data
                                image = Image.open(BytesIO(image_data))

                                # Calculate the aspect ratio to preserve the image's proportions
                                width, height = image.size
                                aspect_ratio = width / height

                                # Scale the image to a width of 300 pixels while maintaining the aspect ratio
                                scaled_width = 300
                                scaled_height = int(scaled_width / aspect_ratio)
                                image = image.resize((scaled_width, scaled_height))

                                # Create a thumbnail of size 300x200 pixels
                                thumbnail = image.copy()
                                thumbnail.thumbnail((width, height))
                                image_datas_Log.append(thumbnail)
                                image_ids_Log.append(image_id)
                                timestamps_Log.append(timestamp)
                                plate_formats_Log.append(plate_format)
                            except Exception as e:
                                print(f"Error displaying the image: {e}")
                    query = "SELECT id, image_data, timestamp, plate_format FROM license_plates_access_accepted;"
                    c.execute(query)
                    results = c.fetchall()
                    for result in results:
                            image_id = result[0]
                            image_data = result[1]
                            timestamp = result[2]
                            plate_format = result[3]
                            try:  

                                image_ids_Accepted.append(image_id)
                                timestamps_Accepted.append(timestamp)
                                plate_formats_Accepted.append(plate_format)
                            except Exception as e:
                                print(f"Error displaying the image: {e}")       
                            c.close()
                            conn.close()
                    print(image_ids_Accepted)
                    print(image_ids_Log)
                except psycopg2.Error as e:
                    print("Error connecting to the database:")
                    print(e)        
                print("datenbanken wurden Aktualisiert")
                return image_datas_Log,image_ids_Log,timestamps_Log,plate_formats_Log,image_ids_Accepted,timestamps_Accepted,plate_formats_Accepted
        
        def check_for_updates(plate_formats_Log_old,
                               plate_formats_Accepted_old):
             # Retrieve the latest data
             image_datas_Log,image_ids_Log,timestamps_Log,plate_formats_Log,image_ids_Accepted,timestamps_Accepted,plate_formats_Accepted = DatabaseManager.retrieve_images_from_database()

             # Compare with the previous data
             if plate_formats_Log_old != plate_formats_Log or plate_formats_Accepted_old != plate_formats_Accepted:
                 # Data has changed, update the UI
                 return True

            # # Update the previous data
            # self.previous_data = latest_data

            # # Schedule the next update check
            # self.after(5000, self.check_for_updates)