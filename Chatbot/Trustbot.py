import tkinter as tk
from tkinter import scrolledtext
import random
import spacy
import speech_recognition as sr
from datetime import datetime


nlp = spacy.load("en_core_web_sm")


INTENTS = {
    "greeting": ["hi", "hello", "hey","hie"],
    "name": ["what is your name", "who are you"],
    "mood": ["how are you", "how's it going", " how you doing"],
    "school": ["how is school", "tell me about your studies"],
    "home": ["how is home", "do you live somewhere"],
    "work": ["do you work", "how's work"],
    "sports": ["do you like sports", "football", "basketball", 
               "what's your favorite sport", "who is your favorite player"],
    "tech": ["do you like tech", "what do you think of ai", 
             "what is programming", "explain machine learning", 
             "how does ai work", "what is an algorithm"],
    "bye": ["bye", "goodbye", "see you later"]
}

RESPONSES = {
    "greeting": ["Hey there!", "Hello!", "Hi!"],
    "name": ["I'm TrustBot, built by Trust."],
    "mood": ["I'm feeling great, thanks for asking!"],
    "school": ["School's a grind but worth it!", 
               "Always learning, always growing."],
    "home": ["Home is peace and Wi-Fi."],
    "work": ["Working hard or hardly working?"],
    "sports": [
        "Football’s my top pick — I like analyzing plays and strategy.",
        "Basketball is fast and intense! Who's your favorite player?",
        "I'm more of a Messi guy — smooth and tactical.",
        "CR7 or Messi? The debate never ends!"
    ],
    "tech": [
        "AI is like giving machines a brain — I’m kind of one myself 😉.",
        "Machine learning is when computers learn from data instead of being manually programmed.",
        "Programming is just giving instructions to machines in a language they understand — like Python or JavaScript.",
        "An algorithm is a set of steps to solve a problem, kind of like a recipe.",
        "AI learns from patterns — give it enough data, and it’ll make decisions or predictions."
    ],
    "bye": ["Goodbye! Catch you later.", "See ya! Stay sharp."],
    "default": ["Hmm, I didn't understand that. Try another topic like tech or sports."]
}

def get_intent(user_input):
    doc1 = nlp(user_input.lower())
    max_score = 0.7
    best_intent = "default"

    for intent, examples in INTENTS.items():
        for example in examples:
            doc2 = nlp(example)
            score = doc1.similarity(doc2)
            if score > max_score:
                max_score = score
                best_intent = intent
    return best_intent

def log_conversation(user_input, bot_response):
    with open("chat_history.txt", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] You: {user_input}\n")
        f.write(f"[{timestamp}] TrustBot: {bot_response}\n")

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TrustBot")
        self.root.geometry("600x500")
       

        self._setup_widgets()
        self.display_message("TrustBot", 
            "Hey! I can hold basic conversations, Let's talk about school,work, sports, and tech too. "
            "Type or say something!"
        )

    def _setup_widgets(self):
        self.chat_log = scrolledtext.ScrolledText(
            self.root, 
            state='disabled', 
            width=60, 
            height=20, 
            wrap='word', 
            font=("Arial", 12),
            bg="#6c7e7f"
        )
        self.chat_log.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.entry = tk.Entry(
            input_frame, 
            font=("Arial", 12), 
            width=50,
            relief=tk.GROOVE,
            borderwidth=2
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_frame, 
            text="Send", 
            command=self.send_message, 
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED
        )
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.voice_button = tk.Button(
            input_frame, 
            text="🎤 Voice", 
            command=self.listen_voice, 
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            relief=tk.RAISED
        )
        self.voice_button.pack(side=tk.LEFT)

    def display_message(self, sender, message):
        self.chat_log.config(state='normal')
        if sender == "TrustBot":
            self.chat_log.insert(tk.END, f"{sender}: ", "bot_tag")
        else:
            self.chat_log.insert(tk.END, f"{sender}: ", "user_tag")
        self.chat_log.insert(tk.END, f"{message}\n")
        self.chat_log.config(state='disabled')
        self.chat_log.see(tk.END)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if user_input:
            self.respond(user_input)
            self.entry.delete(0, tk.END)

    def respond(self, user_input):
        self.display_message("You", user_input)
        intent = get_intent(user_input)
        bot_response = random.choice(RESPONSES[intent])
        self.display_message("TrustBot", bot_response)
        log_conversation(user_input, bot_response)
        if intent == "bye":
            self.root.after(1500, self.root.destroy)

    def listen_voice(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        try:
            with mic as source:
                self.display_message("TrustBot", "Listening...")
                audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            self.respond(user_input)
        except sr.WaitTimeoutError:
            self.display_message("TrustBot", "Didn't hear anything.")
        except sr.UnknownValueError:
            self.display_message("TrustBot", "Couldn't understand you.")
        except sr.RequestError:
            self.display_message("TrustBot", "Voice service not available.")

if __name__ == "__main__":
    root = tk.Tk()
    root.tk_setPalette(background='#ffffff')
    root.option_add('*Font', 'Arial 12')
    app = ChatbotGUI(root)
    root.mainloop()
    
