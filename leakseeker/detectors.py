import math
import re
from typing import List


class EntropyDetector:
    """Detect high-entropy strings that might be secrets"""

    # Stronger patterns
    _BASE64_PATTERN = re.compile(r'\b(?:[A-Za-z0-9+/]{4}){6,}(?:==|=)?\b')
    _HEX_PATTERN = re.compile(r'\b[0-9a-fA-F]{32,}\b')

    def shannon_entropy(self, data: str) -> float:
        if not data:
            return 0.0

        length = len(data)
        freq = {}

        for ch in data:
            freq[ch] = freq.get(ch, 0) + 1

        return -sum(
            (count / length) * math.log2(count / length)
            for count in freq.values()
        )

    def detect_high_entropy(self, text: str) -> List[str]:
        matches = []
        seen = set()

        for pattern, threshold in (
            (self._BASE64_PATTERN, 4.7),  # stricter
            (self._HEX_PATTERN, 3.5),     # hex naturally lower entropy
        ):
            for match in pattern.finditer(text):

                candidate = match.group()

                # 🔥 Length filter
                if not (20 <= len(candidate) <= 300):
                    continue

                if candidate in seen:
                    continue

                unique_chars = len(set(candidate))

                # 🔥 Fast reject (cheap)
                if unique_chars < 6:
                    continue

                lower = candidate.lower()

                # 🔥 Ignore fake/test values
                if any(x in lower for x in (
                    "example", "test", "dummy",
                    "placeholder", "sample", "fake"
                )):
                    continue

                # 🔥 Skip obvious hex patterns (like hashes in logs)
                if pattern == self._HEX_PATTERN and unique_chars < 10:
                    continue

                entropy = self.shannon_entropy(candidate)

                # 🔥 Stronger condition
                if entropy >= threshold:
                    seen.add(candidate)
                    matches.append(candidate)

        return matches