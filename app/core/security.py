import secrets
from typing import Final

# Cryptographic token generator
TOKEN_BYTES_LENGTH: Final[int] = 64


def generate_secure_token() -> str:
    """Generate a cryptographically secure URL-safe token."""
    return secrets.token_urlsafe(TOKEN_BYTES_LENGTH)
