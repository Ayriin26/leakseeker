import math
from collections import Counter

IGNORED_VALUES = {
    "example",
    "test",
    "dummy",
    "sample",
    "your_api_key_here",
    "placeholder",
    "xxxx",
    "123456",
    "null",
    "none",
    "changeme",
}

MIN_SECRET_LENGTH = 16
MIN_ENTROPY = 3.5  # Increased from 3.0


def is_repetitive(value: str) -> bool:
    if not value:
        return False

    # Single character repetition (aaaaaa)
    if len(set(value)) == 1:
        return True

    # Pattern repetition (abcabcabc)
    length = len(value)
    for pattern_length in range(1, (length // 2) + 1):
        if length % pattern_length == 0:
            pattern = value[:pattern_length]
            if pattern * (length // pattern_length) == value:
                return True

    return False


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0

    length = len(value)
    counts = Counter(value)

    return -sum(
        (count / length) * math.log2(count / length)
        for count in counts.values()
    )


def is_valid_secret(value: str) -> bool:
    value = value.strip()

    if not value:
        return False

    # Too short
    if len(value) < MIN_SECRET_LENGTH:
        return False

    value_lower = value.lower()

    # Known dummy / placeholder values
    if any(ignored in value_lower for ignored in IGNORED_VALUES):
        return False

    # Repetitive patterns
    if is_repetitive(value):
        return False

    entropy = shannon_entropy(value)

    # Low entropy → not a real secret
    if entropy < MIN_ENTROPY:
        return False

    # 🔥 Character diversity check
    has_upper = any(c.isupper() for c in value)
    has_lower = any(c.islower() for c in value)
    has_digit = any(c.isdigit() for c in value)
    has_symbol = any(not c.isalnum() for c in value)

    diversity_score = sum([has_upper, has_lower, has_digit, has_symbol])

    # Require at least 2 types (real secrets are mixed)
    if diversity_score < 2:
        return False

    # 🔥 Unique character check
    if len(set(value)) < max(5, len(value) // 4):
        return False

    # 🔥 Reject simple alphabetic strings
    if value.isalpha() and len(value) < 32:
        return False

    return True