from pydantic import BaseModel

class Message(BaseModel):
    text: str

class BotResponse(BaseModel):
    response: str
    score: float