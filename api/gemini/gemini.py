"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not set. Please set it in your environment or .env file."
    )

genai.configure(api_key=GEMINI_API_KEY)

# Generation configuration (tweak as needed)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}


def _create_model():
    """Create a GenerativeModel instance using the configured model name."""
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=generation_config,
        system_instruction=(
            "Eres un traductor de idioma. Solo recibes una entrada y tu salida es traducirlo "
            "al idioma que se te indique. La sintaxis será la siguiente: frase - idioma y respondes "
            "con solo la traducción sin argumentar más nada ni decir otra cosa. Otra sintaxis "
            "también válida es la siguiente: frase - código del idioma. Los código de idioma son: "
            "en para inglés, es para español y otros que te agreguen."
        ),
    )


def _start_chat_session():
    """Start a chat session with a small canned history to help the model's behavior."""
    model = _create_model()
    history = [
        {"role": "user", "parts": ["Manzana - inglés"]},
        {"role": "model", "parts": ["Apple \n"]},
        {"role": "user", "parts": ["Mañana iré al gimnasio - inglés"]},
        {"role": "model", "parts": ["I will go to the gym tomorrow. \n"]},
        {"role": "user", "parts": ["I'm a developer - spanish"]},
        {"role": "model", "parts": ["Soy un desarrollador. \n"]},
        {"role": "user", "parts": ["Tomorrow - es"]},
        {"role": "model", "parts": ["Mañana \n"]},
    ]
    return model.start_chat(history=history)


def translate(text: str, from_lang: str, to_lang: str) -> str:
    """Translate `text` from `from_lang` to `to_lang` using the configured Gemini model.

    Notes:
    - Uses the `GEMINI_MODEL_NAME` environment variable if provided, otherwise defaults to `gemini-1.5`.
    - If the model is not found or unsupported for the requested API method, the function
      catches the 404 and will try to list available models and raise a helpful error.
    """
    try:
        chat_session = _start_chat_session()
        # We send the text followed by a dash and the language indicator as in your examples
        response = chat_session.send_message(f"{text} - {to_lang}")
        return response.text

    except google_exceptions.NotFound as e:
        # Model name is invalid or not supported for this API method. Do not attempt to
        # list models here because the ListModels call may also be unsupported for this
        # API/version credentials. Instead, instruct the caller to use the /models route
        # which will attempt to list models separately.
        raise RuntimeError(
            f"Model '{MODEL_NAME}' not found or unsupported. Call GET /models to see available models or set GEMINI_MODEL_NAME to a supported model."
        ) from e

    except Exception as e:
        # Bubble up an informative runtime error for the caller to handle/log
        raise RuntimeError(f"Error generating translation: {e}") from e


def list_available_models():
    """Return a list of available model names from the GenAI SDK.

    Returns a list of strings. If listing fails, raises a RuntimeError with details.
    """
    try:
        available = genai.list_models()
        names = []
        for m in available:
            name = getattr(m, "name", None) or getattr(m, "model_name", None) or str(m)
            names.append(name)
        return names
    except Exception as e:
        raise RuntimeError(f"Listing models failed: {e}") from e
