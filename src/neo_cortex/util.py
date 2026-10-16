import hashlib
import re
import time
import uuid


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def now_ms() -> int:
    return int(time.time() * 1000)


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def normalize_key(name: str) -> str:
    """Entity key: casefolded, punctuation and whitespace collapsed to single spaces; letters of every script kept."""
    return re.sub(r"[\W_]+", " ", name.casefold()).strip()
