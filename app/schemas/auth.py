from pydantic import BaseModel, EmailStr, Field as PydanticField


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    company_name: str = PydanticField(min_length=2)
    nit: str = PydanticField(min_length=5)
    sector: str = PydanticField(min_length=2)
    size: str = PydanticField(pattern="^(pequena|mediana|grande)$")
    contact_name: str = PydanticField(min_length=2)
    email: EmailStr
    password: str = PydanticField(min_length=5)


class UserOut(BaseModel):
    email: str
    name: str
    role: str
    company_id: int | None = None
    company_name: str | None = None