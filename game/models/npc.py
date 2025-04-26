from __init__ import db
import google.generativeai as genai

# url to find key hopefully?
genai.configure(api_key='https://ai.google.dev/competition/projects/multimodal-gemini-15-flash-api')


class NPC(db.Model):
    __tablename__ = 'NPC'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    greeting = db.Column(db.String(128), unique=True, nullable=False)
    chat_enabled = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, greeting, chat_enabled=False):
        self.name = name
        self.greeting = greeting
        self.chat_enabled = chat_enabled

    def speak(self):
        return f"{self.name}: '{self.dialog}'"

    def chat(self, command):
        if not self.chat_enabled:
            return self.speak()
        return ask_gemini(command, self.name)


def ask_gemini(command, npc_name='Guide'):
    model = genai.GenerativeModel("gemini-1.5-flash")
    convo = model.start_chat(
        history=[
            {
                "role": "system",
                "parts": [
                    f"You are a wise and helpful NPC named {npc_name} in a medieval fantasy world. "
                    f"Stay in character and provide immersive responses."]
            }
        ]
    )
    response = convo.send_message(command)
    return response.text
