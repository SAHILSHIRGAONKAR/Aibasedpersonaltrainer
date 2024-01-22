import speech_recognition as sr

from gtts import gTTS
import os
import pygame
from io import BytesIO
from playsound import playsound

language = 'en'
output_dir = "static/TestVideosAndImages"

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Please say something....")
        audio = recognizer.listen(source, timeout=2)
        try:
            print("You said: \n" + recognizer.recognize_google(audio))
            return (recognizer.recognize_google(audio))
        except Exception as e:
            print("Error: " + str(e))

def text_to_speech(text):
    output_path = os.path.join(output_dir, "output.mp3")
    output = gTTS(text=text, lang=language, slow=False)
    output.save(output_path)

    if os.path.isfile(output_path):
        pygame.mixer.init()
        pygame.mixer.music.load(output_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
    else:
        print("Failed to generate 'output.mp3'")



def main():
    text_to_speech("This the test audio file which will be saved as output.mp3")

if __name__ == "__main__":
    main()