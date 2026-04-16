import re
from typing import List, TypedDict, Literal
from urllib.parse import urlparse, ParseResult


class EndpointResult(TypedDict):
    value: str
    risk: Literal["low", "medium", "high"]


class EndpointDetector:
    """Detect web endpoints and classify risk"""

    URL_PATTERN = re.compile(
        r'https?://[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+'
    )

    PATH_PATTERN = re.compile(
        r'["\'](/(api|admin|internal|debug|auth|graphql|private|management|v[0-9]+)[^"\']*)["\']'
    )

    INTERNAL_KEYWORDS: frozenset[str] = frozenset({
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "::1",
        "[::1]",
        "10.",
        "192.168.",
        "172.16."
    })

    HIGH_RISK_PORTS: frozenset[str] = frozenset({
        "3000", "5000", "8000", "8080", "9000", "9090"
    })

    HIGH_RISK_PATHS: frozenset[str] = frozenset({
        "admin", "internal", "debug", "private"
    })

    def detect(self, text: str) -> List[EndpointResult]:
        results: List[EndpointResult] = []

        seen_urls = set()
        seen_paths = set()

        # -------------------------
        # URL detection
        # -------------------------
        for match in self.URL_PATTERN.finditer(text):
            url = match.group().rstrip(".,;)")

            parsed = urlparse(url)
            if not parsed.netloc:
                continue

            if url in seen_urls:
                continue
            seen_urls.add(url)

            results.append({
                "value": url,
                "risk": self.classify(parsed)
            })

        # -------------------------
        # Path detection
        # -------------------------
        for match in self.PATH_PATTERN.finditer(text):
            path = match.group(1)
            prefix = match.group(2)

            if path in seen_paths:
                continue
            seen_paths.add(path)

            risk = "high" if prefix in self.HIGH_RISK_PATHS else "medium"

            results.append({
                "value": path,
                "risk": risk
            })

        return results

    def classify(self, parsed_url: ParseResult) -> Literal["low", "medium", "high"]:
        full_url = parsed_url.geturl().lower()

        # Split URL into clean tokens (safe boundaries)
        tokens = re.split(r'[/:.\-_\[\]]+', full_url)

        # -------------------------
        # HIGH risk checks
        # -------------------------

        # Internal networks / loopback
        if any(keyword in full_url for keyword in self.INTERNAL_KEYWORDS):
            return "high"

        # High-risk path segments
        if any(token in self.HIGH_RISK_PATHS for token in tokens):
            return "high"

        # Suspicious ports
        if parsed_url.port and str(parsed_url.port) in self.HIGH_RISK_PORTS:
            return "high"

        # -------------------------
        # MEDIUM risk
        # -------------------------

        # Match API as a standalone token only
        if "api" in tokens:
            return "medium"

        return "low"