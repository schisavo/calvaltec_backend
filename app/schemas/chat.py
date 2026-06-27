from pydantic import BaseModel, Field


class ChatHistoryItem(BaseModel):
    role: str
    content: str


class ChatContext(BaseModel):
    pathname: str = ""
    source: str | None = None
    help_type: str | None = None
    question_id: int | None = None
    question_text: str | None = None
    question_block: str | None = None


class ChatMessageIn(BaseModel):
    message: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    history: list[ChatHistoryItem] = Field(default_factory=list)
    context: ChatContext | None = None
