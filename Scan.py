from pyzbar.pyzbar import decode
from gtts import gTTS
import cv2
import os
import time
def text_to_speech_with_pause(text, pause_between_sentences=1, pause_between_chunks=2):
    chunks = text.split('. ')
    
    for chunk in chunks:
        tts = gTTS(chunk, lang='ne')
        tts.save("temp.mp3")
        os.system("start temp.mp3")
        time.sleep(pause_between_sentences)
        os.remove("temp.mp3")
        cv2.waitKey(pause_between_sentences * 1000)

    cv2.waitKey(pause_between_chunks * 1000)

def load_database(file_path):
    with open(file_path, 'r') as file:
        names = [line.strip() for line in file.readlines()]
    return set(names)

def check_and_speak(name, database):
    if name in database:
        data = f"प्रोग्राममा स्वागत छ।{name}"
        print(f"Name: {name}, {data}")

        # Use the data for text-to-speech with pauses
        text_to_speech_with_pause(data)
    else:
       text_to_speech_with_pause('''सदस्य होइन।
              बीबीयूको सदस्य बन्न चाहानु हुन्छ?
              यसको लागि, कृपया हाम्रो टपरसँग सम्पर्क गर्नुहोस्।''')

def scan_qr_code(frame, database):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    qr_codes = decode(gray)

    for qr_code in qr_codes:
        name = qr_code.data.decode("utf-8")
        print(f"QR Code Data: {name}")

        # Check for QR codes, perform text-to-speech with pauses, and database lookup
        check_and_speak(name, database)

if __name__ == "__main__":
    # Specify the path to the database file
    database_file_path = 'students.txt'

    # Load the database from the file
    database = load_database(database_file_path)

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