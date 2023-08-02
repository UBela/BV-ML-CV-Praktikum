import os
import psycopg2
from PIL import Image
from io import BytesIO
from torch.utils.data import Dataset
from datetime import datetime
import io
import tkinter as tk
from PIL import ImageTk, Image

def check_database_connection():
    try:
        # Verbindung zur PostgreSQL-Datenbank herstellen
        conn = psycopg2.connect(
            host="snuffleupagus.db.elephantsql.com",
            port="5432",
            database="lvyoqndm",
            user="lvyoqndm",
            password="X8HtTPeJRhM89GYr8s36GrBnp5aOI9P2"
        )

        # Cursor erstellen
        c = conn.cursor()

        # SQL-Abfrage ausführen (zum Beispiel SELECT version() für die PostgreSQL-Version)
        c.execute("SELECT version();")
        result = c.fetchone()
        print("Verbindung zur Datenbank hergestellt:")
        print(result)

        # Verbindung zur Datenbank beenden
        c.close()
        conn.close()

    except psycopg2.Error as e:
        print("Fehler bei der Verbindung zur Datenbank:")
        print(e)

# Funktion aufrufen, um die Verbindung zur Datenbank zu überprüfen
check_database_connection()


# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(
     host="snuffleupagus.db.elephantsql.com",
     port="5432",
     database="lvyoqndm",
     user="lvyoqndm",
     password="X8HtTPeJRhM89GYr8s36GrBnp5aOI9P2"
)
print(conn)
# Cursor erstellen
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS license_plates_access_log (
        id SERIAL PRIMARY KEY,
        image_data BYTEA,
        label VARCHAR(50),
        access BOOLEAN,
        timestamp TIMESTAMP,
        plate_format VARCHAR(20),
        sightings_count INTEGER DEFAULT 0
    );
""")
c.execute("""
    CREATE TABLE IF NOT EXISTS license_plates_access_accepted (
        id SERIAL PRIMARY KEY,
        image_data BYTEA,
        label VARCHAR(50),
        timestamp TIMESTAMP,
        plate_format VARCHAR(20),
        sightings_count INTEGER DEFAULT 0
    );
""")
c.execute("DELETE FROM license_plates_access_log;")
c.execute("DELETE FROM license_plates_access_accepted;")
print("Daten werden bei jedem Aufruf gelöscht")
conn.commit()


# Funktion zum Hochladen der Bilder in die Datenbank (mit Timestamp, Kennzeichenformat und Sichtungszähler)

def upload_images_to_database(image_dir):
    image_files = [file for file in os.listdir(image_dir) if file.endswith('.jpg') or file.endswith('.png')]
    success_count = 0

    # Verbindung zur Datenbank herstellen
    conn = psycopg2.connect(
     host="snuffleupagus.db.elephantsql.com",
     port="5432",
     database="lvyoqndm",
     user="lvyoqndm",
     password="X8HtTPeJRhM89GYr8s36GrBnp5aOI9P2"
)
    c = conn.cursor()

    # Liste mit möglichen Kennzeichen
    plate_formats = ['SHG-LF206', 'DEF-456', 'GHI-789', 'JKL-012', 'ABC-123', 'XYZ-789', 'MNO-987']

    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        image_data = open(image_path, 'rb').read()

        try:
            # Aktuelles Datum und Uhrzeit als Timestamp erhalten
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Standardwert für plate_format auswählen
            default_plate_format = plate_formats[success_count ]

            # Bild in die Datenbank laden und Timestamp sowie plate_format hinzufügen
            c.execute("""
                INSERT INTO license_plates_access_log (image_data, timestamp, plate_format) VALUES (%s, %s, %s);
            """, (psycopg2.Binary(image_data), timestamp, default_plate_format))
            conn.commit()

            success_count += 1
            print(f"Datei '{image_file}' erfolgreich hochgeladen. Standard-Kennzeichen: {default_plate_format}")
        except psycopg2.Error as e:
            print(f"Fehler beim Hochladen der Datei '{image_file}': {e}")

    # Verbindung zur Datenbank schließen
    c.close()
    conn.close()

    print(f"Gesamtanzahl der erfolgreich hochgeladenen Dateien: {success_count}")

# Bilder in die Datenbank hochladen
upload_images_to_database("TestImagesSet1")


c.close()
conn.close()

#####################################################################################


import tkinter as tk
from PIL import Image, ImageTk
import psycopg2
from io import BytesIO

IMAGE_WIDTH = 320
IMAGE_HEIGHT = 200
IMAGES_PER_ROW = 3

def retrieve_images_from_database():
    try:
        # Verbindung zur PostgreSQL-Datenbank herstellen
        conn = psycopg2.connect(
            host="snuffleupagus.db.elephantsql.com",
            port="5432",
            database="lvyoqndm",
            user="lvyoqndm",
            password="X8HtTPeJRhM89GYr8s36GrBnp5aOI9P2"
        )

        # Cursor erstellen
        c = conn.cursor()

        # SQL-Abfrage zum Abrufen aller Bilder aus der Tabelle license_plates_access_log
        query = "SELECT image_data, timestamp FROM license_plates_access_log;"
        c.execute(query)
        results = c.fetchall()

        images = []
        for result in results:
            image_data = result[0]
            timestamp = result[1]

            try:
                # Image-Objekt aus den binären Daten erstellen und in gewünschte Größe konvertieren
                image = Image.open(BytesIO(image_data))
                image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
                images.append((image, timestamp))
            except Exception as e:
                print(f"Fehler beim Anzeigen des Bildes: {e}")

        # Verbindung zur Datenbank beenden
        c.close()
        conn.close()

        return images

    except psycopg2.Error as e:
        print("Fehler bei der Verbindung zur Datenbank:")
        print(e)

def show_images():
    images = retrieve_images_from_database()

    # Create the GUI window
    window = tk.Tk()
    window.title("Image Gallery")
    window.configure(bg="black") 
    # Frame for the images
    image_frame = tk.Frame(window)
    image_frame.pack()
    

    row_frame = None
    for i, (image, timestamp) in enumerate(images):
        # Convert the image to a Tkinter-compatible format
        photo = ImageTk.PhotoImage(image)

        # Create a Label to display the image
        label = tk.Label(image_frame, image=photo)
        label.pack(side=tk.LEFT, padx=10, pady=10)

        # Save a reference to the image object to prevent it from being garbage collected
        label.image = photo

        # Create a Button
        button = tk.Button(image_frame, text="Submit", width=5, height=5, fg="royalblue4", bg="lavender",
                           font=("Helvetica", 10, "bold italic"))
        button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

        # Create a Label for the timestamp
        timestamp_label = tk.Label(image_frame, text=timestamp)
        timestamp_label.pack(side=tk.LEFT, padx=10, pady=(0, 10))

        # Start a new row if the maximum number of images per row is reached
        if (i + 1) % IMAGES_PER_ROW == 0:
            row_frame = tk.Frame(window)
            row_frame.pack()

    # Center the window on the screen
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Fenster anzeigen
    window.mainloop()


#



# Funktion aufrufen, um Bilder anzuzeigen
show_images()

