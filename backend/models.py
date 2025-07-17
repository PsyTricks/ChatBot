from pydantic import BaseModel

class Message(BaseModel):
    text: str

class BotResponse(BaseModel):
    response: str
    matched_keywords: list[str]
    score: int