import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

_store: dict[str, tuple[str, datetime]] = {}

TTL_SECONDS = 30

def generate_code(jwt: str) -> str:
    """Génère un code jetable associé au JWT, valable 30 secondes."""
    code = secrets.token_urlsafe(32)
    expiry = datetime.now(timezone.utc) + timedelta(seconds=TTL_SECONDS)
    _store[code] = (jwt, expiry)
    return code


def consume_code(code: str) -> Optional[str]:
    """
    Échange le code contre le JWT.
    Retourne None si le code est inconnu ou expiré.
    Le code est supprimé immédiatement après usage (one-shot).
    """
    entry = _store.pop(code, None)
    if entry is None:
        return None

    jwt, expiry = entry
    if datetime.now(timezone.utc) > expiry:
        return None

    return jwt