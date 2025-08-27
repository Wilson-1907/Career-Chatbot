import random


def generate_otp(length: int = 4) -> str:
    """Return a numeric OTP as a string, e.g., '4831'."""
    start = 10 ** (length - 1)
    end = (10 ** length) - 1
    return str(random.randint(start, end))
