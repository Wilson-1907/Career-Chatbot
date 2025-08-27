from datetime import datetime, timedelta


def fake_issue_token(user_id: str) -> dict:
    """Temporary fake token payload (replace with real JWT later)."""
    return {
        "access_token": f"token-{user_id}",
        "token_type": "bearer",
        "expires_at": (datetime.utcnow() + timedelta(minutes=60)).isoformat() + "Z",
    }
