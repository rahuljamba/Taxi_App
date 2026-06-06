# Pip installation commands:
# pip install opencv-python SpeechRecognition word2number pyaudio

import cv2
import threading
import speech_recognition as sr
from word2number import w2n

# Global variables
detected_number = ""
data_lock = threading.Lock()

def recognize_whispers_background():
    global detected_number
    
    recognizer = sr.Recognizer()
    
    # Threshold ko thoda balance kiya hai (300) taaki normal noise ignore ho aur whisper catch ho
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = False
    
    with sr.Microphone() as source:
        print("\n--- Mic Environment Setup ---")
        print("Adjusting for ambient noise... Please stay quiet for 2 seconds.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Setup Done! Start speaking or whispering numbers (e.g., 'one', 'two')...\n")
        
        while True:
            try:
                print("Listening... (Speak now)")
                # listen timeout aur phrase limit ko optimize kiya hai
                audio_data = recognizer.listen(source, timeout=None, phrase_time_limit=3)
                
                print("Processing voice with Google API...")
                spoken_text = recognizer.recognize_google(audio_data).lower()
                print(f"👉 Console Log (Google Heard): '{spoken_text}'")
                
                # Check text for numbers
                try:
                    num_val = w2n.word_to_num(spoken_text)
                    print(f"✅ Successfully converted to numeric: {num_val}")
                    
                    with data_lock:
                        detected_number = str(num_val)
                        
                except ValueError:
                    # Agar "one" ki jagah kuch aur suna, toh check karo kahin string mein number toh nahi chupa
                    print("❌ Word is not a direct number. Retrying...")
                    pass
                    
            except sr.UnknownValueError:
                print("Listening status: Audio received but couldn't understand the word. Try speaking clearly.")
                pass
            except sr.RequestError as e:
                print(f"Network Error: Google API service down or no internet; {e}")
            except Exception as e:
                print(f"Error inside loop: {e}")

def main():
    global detected_number
    
    # Background thread check
    bg_thread = threading.Thread(target=recognize_whispers_background, daemon=True)
    bg_thread.start()
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Webcam open nahi ho raha.")
        return

    print("Webcam live feed running. Press 'q' on the camera window to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
            
        with data_lock:
            current_display_num = detected_number

        # Screen par display logic
        if current_display_num:
            display_text = f"Number: {current_display_num}"
            # UI text ko aur bada aur bright green kiya hai taaki clear dikhe
            cv2.putText(frame, display_text, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4, cv2.LINE_AA)

        cv2.imshow("Live Whisper Number Recognition", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()