from fastapi import FastAPI
from scoring import get_response
from models import Message
import json

app = FastAPI()

'''Basic initial endpoint'''
@app.post("/ask")
def resolve(message: Message):
    result = get_response(message.text)
    return result
