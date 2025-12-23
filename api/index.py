from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .gemini import translate, list_available_models

app = FastAPI()

# Allow all CORS origins (use carefully in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


@app.get('/models')
async def models():
    try:
        names = list_available_models()
        return {"models": names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/')
async def index(input:TranslateModel):
    try:
        return translate(input.text, input.from_lang, input.to_lang)
    except Exception as e:
        # Raise an HTTP 500 with the error message for easier debugging
        raise HTTPException(status_code=500, detail=str(e))
