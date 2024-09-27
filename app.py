import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os
import tkinter as tk
from tkinter import messagebox, StringVar

# Function to listen to speech
def listen_to_speech(input_language):
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)  
            text = recognizer.recognize_google(audio, language=input_language)  
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results; {e}")
            return None
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None

# Function to translate text
def translate_text(text, target_language):
    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_language)
        print(f"Translated text: {translated.text}")
        return translated.text
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {e}")
        return None

# Function to convert text to speech
def speak_text(text, language):
    try:
        tts = gTTS(text=text, lang=language)
        filename = "temp_audio.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        messagebox.showerror("Error", f"Speech synthesis failed: {e}")

# Function to handle the process
def start_process():
    input_lang = input_language_var.get()
    text = listen_to_speech(input_language=input_lang)
    
    if text:
        target_lang = output_language_var.get()
        translated_text = translate_text(text, target_language=target_lang)
        if translated_text:
            result_label.config(text=f"Detected: {text}\nTranslated: {translated_text}")
            speak_text(translated_text, language=target_lang)


root = tk.Tk()
root.title("Speech to Text Translator")
root.geometry("400x400")


languages = {
    "English": "en-IN",
    "Telugu": "te",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de"
}

# Create GUI elements
title_label = tk.Label(root, text="Speech to Text Translator", font=("Helvetica", 16))
title_label.pack(pady=10)

instructions_label = tk.Label(root, text="Click the button and speak", font=("Helvetica", 12))
instructions_label.pack(pady=5)

# Input language selection dropdown
input_language_var = StringVar(root)
input_language_var.set(languages["English"])  

input_language_label = tk.Label(root, text="Choose Input Language", font=("Helvetica", 12))
input_language_label.pack(pady=5)

# Create a list of language names for the dropdown
input_languages_names = list(languages.keys())
input_language_menu = tk.OptionMenu(root, input_language_var, *input_languages_names)
input_language_menu.pack(pady=5)

# Output language selection dropdown
output_language_var = StringVar(root)
output_language_var.set(languages["Telugu"])  

output_language_label = tk.Label(root, text="Choose Translation Language", font=("Helvetica", 12))
output_language_label.pack(pady=5)

# Create a list of language names for the dropdown
output_languages_names = list(languages.keys())
output_language_menu = tk.OptionMenu(root, output_language_var, *output_languages_names)
output_language_menu.pack(pady=5)

# Button to start the speech recognition
start_button = tk.Button(root, text="Start Listening", command=start_process, font=("Helvetica", 14))
start_button.pack(pady=20)

# Label to show results
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)


root.mainloop()
