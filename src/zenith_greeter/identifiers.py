"""UUID, short identifier and secure token generation."""
import secrets
import string
import uuid

def uuid4():
    """Return a random UUID4 string."""
    return str(uuid.uuid4())

def short_id(length=8, alphabet=string.ascii_letters + string.digits):
    """Return a compact cryptographically secure identifier."""
    if not isinstance(length, int) or isinstance(length, bool) or length < 1:
        raise ValueError("length must be a positive integer")
    if not isinstance(alphabet, str) or len(set(alphabet)) < 2:
        raise ValueError("alphabet must contain at least two distinct characters")
    return "".join(secrets.choice(alphabet) for _ in range(length))

def numeric_id(length=8):
    """Return a numeric identifier as a string, preserving leading zeroes."""
    if not isinstance(length, int) or isinstance(length, bool) or length < 1:
        raise ValueError("length must be a positive integer")
    return "".join(secrets.choice(string.digits) for _ in range(length))

def random_token(length=32):
    """Return a URL-safe cryptographically secure token of requested length."""
    if not isinstance(length, int) or isinstance(length, bool) or length < 1:
        raise ValueError("length must be a positive integer")
    alphabet = string.ascii_letters + string.digits + "-_"
    return "".join(secrets.choice(alphabet) for _ in range(length))
