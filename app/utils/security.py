import hashlib
import hmac
import secrets
import base64
import json
import os
import time


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return f"{salt}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, expected = stored_hash.split("$", 1)
    except ValueError:
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000).hex()
    return hmac.compare_digest(actual, expected)


def create_access_token(user_id: int, role: str) -> str:
    header = _encode({"alg": "HS256", "typ": "JWT"})
    payload = _encode({"sub": str(user_id), "role": role, "exp": int(time.time()) + 60 * 60 * 8})
    signature = _sign(f"{header}.{payload}")
    return f"{header}.{payload}.{signature}"


def decode_access_token(token: str) -> dict:
    try:
        header, payload, signature = token.split(".")
        if not hmac.compare_digest(signature, _sign(f"{header}.{payload}")):
            raise ValueError("Invalid signature")
        claims = json.loads(_decode(payload))
        if claims.get("exp", 0) < time.time():
            raise ValueError("Token expired")
        return claims
    except (ValueError, TypeError, json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("Invalid token")


def _encode(value: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(value, separators=(",", ":")).encode()).decode().rstrip("=")


def _decode(value: str) -> str:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)).decode()


def _sign(value: str) -> str:
    secret = os.getenv("JWT_SECRET", "change-this-development-secret")
    digest = hmac.new(secret.encode(), value.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")
