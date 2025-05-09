from __init__ import db
from secret import secrets
from google import genai
from google.genai import types


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
    client = genai.Client(api_key=secrets['gemini_api_key'])

    response = client.models.generate_content(
        model=secrets['gemini_model'],
        config=types.GenerateContentConfig(
            system_instruction=f"You are a wise and helpful NPC named {npc_name} in a medieval fantasy world. "
                               "Stay in character and provide immersive responses."),
        contents=f"The user's input: {command}"
    )

    return response.text
