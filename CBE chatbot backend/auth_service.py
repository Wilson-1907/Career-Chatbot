from typing import Dict
from dataclasses import dataclass

from utils.otp import generate_otp

# In-memory "database" (we'll swap with Supabase later)
_USERS: Dict[str, "User"] = {}   # key = identifier (email or phone)

@dataclass
class User:
    identifier: str
    email: str | None = None
    phone: str | None = None
    otp: str | None = None
    is_verified: bool = False

def request_login(identifier: str, email: str | None, phone: str | None) -> str:
    """Create or fetch user and set OTP."""
    user = _USERS.get(identifier) or User(identifier=identifier, email=email, phone=phone)
    code = generate_otp(4)
    user.otp = code
    _USERS[identifier] = user
    return code

def verify_otp(identifier: str, otp: str) -> bool:
    user = _USERS.get(identifier)
    if not user or not user.otp:
        return False
    if user.otp == otp:
        user.is_verified = True
        user.otp = None   # one-time use
        _USERS[identifier] = user
        return True
    return False
