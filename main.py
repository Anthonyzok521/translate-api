from fastapi import FastAPI
from pydantic import BaseModel
from gemini import translate

app = FastAPI()

class TranslateModel(BaseModel):
    text: str
    from_lang: str
    to_lang: str

@app.post('/')
def index(input:TranslateModel):
    return translate(input.text, input.from_lang, input.to_lang)
