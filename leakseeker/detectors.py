import math
import re
from typing import Optional

class EntropyDetector:
    """Detect high-entropy strings that might be secrets"""

    @staticmethod
    def shannon_entropy(data: str) -> float:
        """Calculate Shannon entropy of a string"""
        if not data:
            return 0

        entropy = 0
        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def detect_high_entropy(self, text: str, threshold: float = 4.0) -> Optional[str]:
        """Detect high-entropy strings that could be secrets"""
        # Look for base64-like strings
        base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'

        for match in re.finditer(base64_pattern, text):
            candidate = match.group()
            if len(candidate) > 30 and self.shannon_entropy(candidate) > threshold:
                return candidate
        return None
