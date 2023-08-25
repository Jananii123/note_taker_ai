import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import openai


# Initialize your OpenAI API key
openai.api_key = "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"


# Global variables
audio = None
recorded_text = ""
r = sr.Recognizer()
conversation_box = None
recording_thread = None

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role" : "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def start_recording():
    global audio, recorded_text, recording_thread
    with sr.Microphone() as source:
        audio = r.listen(source)
    update_conversation_box("Recording done.\n")
    recorded_text = process_audio()
    update_conversation_box(f"You said: {recorded_text}\n")

    recording_thread = None


def stop_recording():
    global recording_thread
    if recording_thread and recording_thread.is_alive():
        recording_thread.join()
        update_conversation_box("Recording stopped.\n")
        recording_thread = None


def take_notes():
    global audio, recorded_text
    recorded_text = process_audio()
    notes = generate_notes(recorded_text)
    update_conversation_box("Notes:\n")
    update_conversation_box(notes + "\n")


def continue_conversation():
    global recorded_text
    if recorded_text:
        openai_chat(recorded_text)


def process_audio():
    try:
        audio_data = audio.get_wav_data()
        text = transcribe_audio(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand what you said."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"


def transcribe_audio(audio_data):
    audio = sr.AudioData(audio_data, sample_rate=44100, sample_width=2)
    return r.recognize_google(audio)


def generate_notes(text):
    
    x = generate_response("Shortly summarize and take notes on the following text:" + text)
    return x


def openai_chat(user_input):
    update_conversation_box("More info:\n")
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    ai_response = response.choices[0].message['content']
    update_conversation_box("AI: " + ai_response + "\n")


def update_conversation_box(text):
    conversation_box.config(state=tk.NORMAL)
    conversation_box.insert(tk.END, text)
    conversation_box.see(tk.END)
    conversation_box.config(state=tk.DISABLED)




def generate_review_questions():
    global recorded_text
    if len(recorded_text) > 0:
        questions = generate_questions(recorded_text)
        update_conversation_box("Review Questions:\n")
        update_conversation_box(questions + "\n")
    else:
        update_conversation_box("No recorded text to generate review questions.\n")


def generate_questions(text):
    z = generate_response("Generate three simple review questions according to the topic:" + text)
    return z

def update_reasources():
    global recorded_text
    if len(recorded_text) > 0:
        reasources1 = get_more_reasources(recorded_text)
        update_conversation_box("more reasources:\n")
        update_conversation_box(reasources1 + "\n")
    else:
        update_conversation_box("No recorded text to get reasources for.\n")
def get_more_reasources(text):
    y = generate_response("give links to online reasources for the following text:" + text)
    return y

def main():
    global conversation_box
    root = tk.Tk()
    root.title("AI Assistant")


    # Define a larger font for buttons
    button_font = ("Helvetica", 14)


    record_button = tk.Button(root, text="Start Recording", command=start_recording, bg="red", font=button_font)
    record_button.pack(side=tk.TOP, padx=10, pady=10)


    stop_record_button = tk.Button(root, text="Stop Recording", command=stop_recording, bg="orange", font=button_font)
    stop_record_button.pack(side=tk.TOP, padx=10, pady=10)


    take_notes_button = tk.Button(root, text="Take Notes", command=take_notes, bg="blue", font=button_font)
    take_notes_button.pack(side=tk.TOP, padx=10, pady=10)


    more_info_button = tk.Button(root, text="More Info", command=continue_conversation, bg="green", font=button_font)
    more_info_button.pack(side=tk.TOP, padx=10, pady=10)


    review_questions_button = tk.Button(root, text="Review Questions", command=generate_review_questions, bg="purple", font=button_font)
    review_questions_button.pack(side=tk.TOP, padx=10, pady=10)

    more_reasources = tk.Button(root, text="More Reasources", command=update_reasources, bg="purple", font=button_font)
    more_reasources.pack(side=tk.TOP, padx=10, pady=10)

    conversation_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=30)
    conversation_box.pack(padx=10, pady=10)


    root.mainloop()

main()
