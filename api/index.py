from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .gemini import translate

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslateModel(BaseModel):
    text: str
    from_lang: str
    to_lang: str

@app.get('/')
async def init():
    return {'message' : 'Initialized'}

@app.post('/')
async def index(input:TranslateModel):
    return translate(input.text, input.from_lang, input.to_lang)
