import os
import psycopg2
from PIL import Image
from io import BytesIO
from torch.utils.data import Dataset
from datetime import datetime
import io
def check_database_connection():
    try:
        # Verbindung zur PostgreSQL-Datenbank herstellen
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
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
     host="localhost",
     port="5432",
     database="postgres"
)
print(conn)
# Cursor erstellen
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS license_plates (
        id SERIAL PRIMARY KEY,
        image_data BYTEA,
        label VARCHAR(50),
        is_accepted BOOLEAN,
        timestamp TIMESTAMP,
        plate_format VARCHAR(20),
        sightings_count INTEGER DEFAULT 0
    );
""")
conn.commit()

# Funktion zum Hochladen der Bilder in die Datenbank (mit Timestamp, Kennzeichenformat und Sichtungszähler)

def upload_images_to_database(image_dir):
    image_files = [file for file in os.listdir(image_dir) if file.endswith('.jpg') or file.endswith('.png')]
    success_count = 0

    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        image_data = open(image_path, 'rb').read()

        try:
            # Aktuelles Datum und Uhrzeit als Timestamp erhalten
            timestamp = datetime.now()

            # Bild in die Datenbank laden und Timestamp hinzufügen
            c.execute("""
                INSERT INTO license_plates (image_data, timestamp) VALUES (%s, %s);
            """, (psycopg2.Binary(image_data), timestamp))
            conn.commit()

            success_count += 1
            print(f"Datei '{image_file}' erfolgreich hochgeladen.")
        except psycopg2.Error as e:
            print(f"Fehler beim Hochladen der Datei '{image_file}': {e}")
    print(f"Gesamtanzahl der erfolgreich hochgeladenen Dateien: {success_count}")


# Bilder in die Datenbank hochladen
upload_images_to_database("TestImagesSet1")

def retrieve_example_image():
    # SQL-Abfrage zum Abrufen des zuletzt hochgeladenen Bildes
    query = "SELECT image_data, timestamp FROM license_plates ORDER BY id DESC LIMIT 1;"
    c.execute(query)
    result = c.fetchone()
    
    if result:
        image_data = result[0]
        timestamp = result[1]
        
        try:
            # Image-Objekt aus den binären Daten erstellen
            image = Image.open(io.BytesIO(image_data))
            image.show()
            
            # Hochladedatum anzeigen
            print("Bild erfolgreich angezeigt.")
            print("Hochgeladen am:", timestamp)
        except Exception as e:
            print(f"Fehler beim Anzeigen des Bildes: {e}")
    else:
        print("Es wurden keine Bilder gefunden.")
# Verbindung zur Datenbank beenden
retrieve_example_image()
c.close()
conn.close()