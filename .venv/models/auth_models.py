from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None

    def identifier(self) -> str:
        # An identifier (email or phone) to index users in memory/DB
        return self.email or self.phone or ""

class VerifyRequest(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    otp: str = Field(..., min_length=4, max_length=6)

class LoginResponse(BaseModel):
    message: str
    otp_preview: str | None = None   # only for dev/testing
