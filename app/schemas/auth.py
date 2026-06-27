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
    id: int | None = None
    email: str
    name: str
    role: str
    company_id: int | None = None
    company_name: str | None = None
    company_email: str | None = None
    company_nit: str | None = None
    company_sector: str | None = None


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserOut


class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str = PydanticField(min_length=5)
    name: str = PydanticField(min_length=2)
    role: str = PydanticField(pattern="^(admin|auditor|company)$")


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class MessageResponse(BaseModel):
    message: str