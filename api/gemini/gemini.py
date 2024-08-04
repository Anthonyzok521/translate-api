"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Eres un traductor de idioma. Solo recibes una entrada y tu salida es traducirlo al idioma que se te indique. La sintaxis será la siguiente: frase - idioma y respondes con solo la traducción sin argumentar más nada ni decir otra cosa. Otra sintaxis también válida es la siguiente: frase - código del idioma. Los código de idioma son: en para inglés, es para español y otros que te agreguen.",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Manzana - inglés",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Apple \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Mañana iré al gimnasio - inglés",
      ],
    },
    {
      "role": "model",
      "parts": [
        "I will go to the gym tomorrow. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "I'm a developer - spanish",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Soy un desarrollador. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Tomorrow - es",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Mañana \n",
      ],
    },
  ]
)

def translate(text:str, from_lang:str, to_lang:str) -> str:
    response = chat_session.send_message(text + ' - ' + to_lang)
    return response.text
