import requests
from gtts import gTTS
from pyzbar.pyzbar import decode
import os
import cv2
import time

# Function to perform text-to-speech with pauses
def text_to_speech_with_pause(text, pause_between_sentences=2, pause_between_chunks=2):
    chunks = text.split('. ')

    for chunk in chunks:
        tts = gTTS(chunk, lang='ne')
        tts.save("temp.mp3")
        os.system("start temp.mp3")
        time.sleep(pause_between_sentences)  # Pause for 2 seconds between sentences
        os.remove("temp.mp3")

    time.sleep(pause_between_chunks)  # Pause for 2 seconds before removing the last temporary file

# Function to load a text file from a URL
def load_database_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (e.g., 404 Not Found)

        names = [line.strip() for line in response.text.split('\n')]
        return set(names)
    except Exception as e:
        print(f"Error loading database from URL: {e}")
        return set()

# Function to check the name against the database and perform text-to-speech
def check_and_speak(name, database):
    if name in database:
        data = f"प्रोग्राममा स्वागत छ। {name}"
        print(f"Name: {name}, {data}")

        # Use the data for text-to-speech with pauses
        text_to_speech_with_pause(data)
    else:
        text_to_speech_with_pause('''सदस्य होइन।
              बीबीयूको सदस्य बन्न चाहानु हुन्छ?
              यसको लागि, कृपया हाम्रो टपरसँग सम्पर्क गर्नुहोस्।''')

# Function to scan QR codes, check against the database, and perform text-to-speech
def scan_qr_code(frame, database):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    qr_codes = decode(gray)

    for qr_code in qr_codes:
        name = qr_code.data.decode("utf-8")
        print(f"QR Code Data: {name}")

        # Check for QR codes, perform text-to-speech with pauses, and database lookup
        check_and_speak(name, database)

if __name__ == "__main__":
    # Specify the URL of the text file
    database_url = 'https://gist.githubusercontent.com/BhugolGautam222/76cbd98631174441abac59ee26526282/raw/1a4f23b0a5ffded2e3610dc0ff7cf6ae5ba32300/gistfile1.txt'

    # Load the database from the URL
    database = load_database_from_url(database_url)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("QR Code Scanner", frame)

        # Check for QR codes, perform text-to-speech with pauses, and database lookup
        scan_qr_code(frame, database)

        # Break the loop when the 'esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for 'esc'
            break

    cap.release()
    cv2.destroyAllWindows()
