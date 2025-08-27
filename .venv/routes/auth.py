from fastapi import APIRouter, HTTPException
from models.auth_models import LoginRequest, VerifyRequest, LoginResponse
from services.auth_service import request_login, verify_otp
from utils.security import fake_issue_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    identifier = payload.identifier()
    if not identifier:
        raise HTTPException(status_code=400, detail="Provide email or phone.")

    otp = request_login(identifier, payload.email, payload.phone)
    # In development we return the OTP so you can test quickly.
    # In production: send via email/SMS and do NOT return it.
    return LoginResponse(message="OTP sent", otp_preview=otp)

@router.post("/verify")
def verify(payload: VerifyRequest):
    identifier = payload.email or payload.phone
    if not identifier:
        raise HTTPException(status_code=400, detail="Provide email or phone.")

    ok = verify_otp(identifier, payload.otp)
    if not ok:
        raise HTTPException(status_code=401, detail="Invalid OTP or user not found.")

    # Issue a fake token for now; replace with real JWT later
    token = fake_issue_token(user_id=identifier)
    return {"message": "Login successful", **token}
