import speech_recognition as sr
import keyboard
import threading

def start_recording():
    global audio
    print("Say something!")
    with sr.Microphone() as source:
        audio = r.listen(source)
    print("Recording done.")
    process_audio()

def process_audio():
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def on_enter(event):
    if event.name == "enter" and event.event_type == keyboard.KEY_DOWN:
        start_recording_thread = threading.Thread(target=start_recording)
        start_recording_thread.start()

r = sr.Recognizer()
audio = None

keyboard.hook(on_enter)

print("Press the Enter key to start recording.")

keyboard.wait('esc')  

keyboard.unhook_all()  



