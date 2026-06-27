from pydantic import BaseModel, Field


class ChatHistoryItem(BaseModel):
    role: str
    content: str


class ChatContext(BaseModel):
    pathname: str = ""


class ChatMessageIn(BaseModel):
    message: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    history: list[ChatHistoryItem] = Field(default_factory=list)
    context: ChatContext | None = None
