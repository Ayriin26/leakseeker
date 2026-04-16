import re
from dataclasses import dataclass
from typing import Pattern, List

@dataclass
class SecretPattern:
    name: str
    pattern: Pattern
    description: str
    risk_level: str  # low, medium, high, critical

def get_patterns() -> List[SecretPattern]:
    return [

        # =========================
        # 🔴 AWS
        # =========================
        SecretPattern(
            name="aws_access_key",
            pattern=re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
            description="AWS Access Key ID",
            risk_level="critical"
        ),
        SecretPattern(
            name="aws_secret_key",
            pattern=re.compile(
                r'(?i)aws.{0,30}(secret|access).{0,10}[=:]\s*[\'\"]([A-Za-z0-9/+]{40})[\'\"]'
            ),
            description="AWS Secret Access Key",
            risk_level="critical"
        ),

        # =========================
        # 🔴 Google / Firebase
        # =========================
        SecretPattern(
            name="google_api_key",
            pattern=re.compile(r'AIza[0-9A-Za-z\-_]{35}'),
            description="Google API Key",
            risk_level="high"
        ),
        SecretPattern(
            name="firebase_url",
            pattern=re.compile(r'https://[a-z0-9-]+\.firebaseio\.com.*auth='),
            description="Firebase Database URL (with auth)",
            risk_level="medium"
        ),

        # =========================
        # 🔴 Stripe / Payments
        # =========================
        SecretPattern(
            name="stripe_key",
            pattern=re.compile(r'\b(sk|pk)_(test|live)_[a-zA-Z0-9]{24,}\b'),
            description="Stripe API Key",
            risk_level="critical"
        ),
        SecretPattern(
            name="razorpay_key",
            pattern=re.compile(r'rzp_(test|live)_[a-zA-Z0-9]{14,}'),
            description="Razorpay API Key",
            risk_level="high"
        ),

        # =========================
        # 🔴 GitHub / Tokens
        # =========================
        SecretPattern(
            name="github_token",
            pattern=re.compile(r'gh[pousr]_[A-Za-z0-9_]{36}'),
            description="GitHub Token",
            risk_level="high"
        ),

        # =========================
        # 🔴 Auth / JWT
        # =========================
        SecretPattern(
            name="jwt_token",
            pattern=re.compile(r'eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+'),
            description="JWT Token",
            risk_level="medium"
        ),
        SecretPattern(
            name="bearer_token",
            pattern=re.compile(r'Bearer\s+[A-Za-z0-9\-._~+/]+=*'),
            description="Bearer Token",
            risk_level="medium"
        ),
        SecretPattern(
            name="jwt_secret",
            pattern=re.compile(
                r'(?i)(jwt[_-]?secret|secret[_-]?key)[\s]*[=:][\s]*[\'\"]?([a-zA-Z0-9]{32,})[\'\"]?'
            ),
            description="JWT Secret Key",
            risk_level="high"
        ),

        # =========================
        # 🔴 Database URLs
        # =========================
        SecretPattern(
            name="database_url",
            pattern=re.compile(r'(?i)(postgres|mysql|mongodb(\+srv)?)://[^\s\'\"]+'),
            description="Database Connection URL",
            risk_level="high"
        ),

        # =========================
        # 🔴 Generic API Keys
        # =========================
        SecretPattern(
            name="api_key",
            pattern=re.compile(
                r'(?i)(api[_-]?key|apikey)[\s]*[=:][\s]*[\'\"]?([a-zA-Z0-9\-_]{20,})[\'\"]?'
            ),
            description="Generic API Key",
            risk_level="high"
        ),
        SecretPattern(
            name="api_secret",
            pattern=re.compile(
                r'(?i)(api[_-]?secret)[\s]*[=:][\s]*[\'\"]?([A-Za-z0-9\-_]{20,})[\'\"]?'
            ),
            description="Generic API Secret",
            risk_level="high"
        ),

        # =========================
        # 🔴 OAuth
        # =========================
        SecretPattern(
            name="oauth_token",
            pattern=re.compile(
                r'(?i)oauth[_-]?token[\s]*[=:][\s]*[\'\"]?([A-Za-z0-9\-_=]{16,64})[\'\"]?'
            ),
            description="OAuth Token",
            risk_level="medium"
        ),

        # =========================
        # 🔴 Slack / Discord
        # =========================
        SecretPattern(
            name="slack_token",
            pattern=re.compile(r'xox[baprs]-[0-9a-zA-Z\-]{10,48}'),
            description="Slack API Token",
            risk_level="high"
        ),
        SecretPattern(
            name="discord_token",
            pattern=re.compile(r'mfa\.[0-9a-zA-Z_\-]{84}'),
            description="Discord Token",
            risk_level="high"
        ),

        # =========================
        # 🔴 Email / SMTP
        # =========================
        SecretPattern(
            name="smtp_password",
            pattern=re.compile(
                r'(?i)(smtp|email)[_-]?password[\s]*[=:][\s]*[\'\"]?([^\s\'\"]+)[\'\"]?'
            ),
            description="SMTP/Email Password",
            risk_level="high"
        ),

        # =========================
        # 🔴 Private Keys (CRITICAL)
        # =========================
        SecretPattern(
            name="private_key",
            pattern=re.compile(r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----'),
            description="Private Key Block",
            risk_level="critical"
        ),

        # =========================
        # 🔴 Crypto Keys (FIXED)
        # =========================
        SecretPattern(
            name="crypto_private_key",
            pattern=re.compile(
                r'(?i)(private[_-]?key|priv[_-]?key)[\s]*[=:][\s]*[\'\"]?[0-9a-fA-F]{64}[\'\"]?'
            ),
            description="Cryptocurrency Private Key",
            risk_level="critical"
        ),
    ]