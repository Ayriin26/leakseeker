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
        # AWS
        SecretPattern(
            name="aws_access_key",
            pattern=re.compile(r'AKIA[0-9A-Z]{16}'),
            description="AWS Access Key ID",
            risk_level="critical"
        ),
        SecretPattern(
            name="aws_secret_key",
            pattern=re.compile(r'(?i)aws_secret(?:_access)?_key\s*[=:]\s*[\'\"]?([A-Za-z0-9/+]{40})[\'\"]?'),
            description="AWS Secret Access Key",
            risk_level="critical"
        ),

        # Stripe
        SecretPattern(
            name="stripe_key",
            pattern=re.compile(r'(?i)(sk|pk)_(test|live)_[a-zA-Z0-9]{24,}'),
            description="Stripe API Key",
            risk_level="critical"
        ),

        # Generic API Keys
        SecretPattern(
            name="api_key",
            pattern=re.compile(r'(?i)(api[_-]?key|apikey)[\s]*[=:][\s]*[\'\"]?([a-zA-Z0-9]{32,45})[\'\"]?'),
            description="Generic API Key",
            risk_level="high"
        ),

        # Database URLs
        SecretPattern(
            name="database_url",
            pattern=re.compile(r'(?i)(postgres|mysql|mongodb)://[a-zA-Z0-9_]+:[a-zA-Z0-9_@!$%^&*()\-_=+]+@[^\s\'\"]+'),
            description="Database Connection URL with credentials",
            risk_level="high"
        ),

        # JWT Secrets
        SecretPattern(
            name="jwt_secret",
            pattern=re.compile(r'(?i)(jwt[_-]?secret|secret[_-]?key)[\s]*[=:][\s]*[\'\"]?([a-zA-Z0-9]{32,})[\'\"]?'),
            description="JWT Secret Key",
            risk_level="high"
        ),

        # OAuth
        SecretPattern(
            name="oauth_token",
            pattern=re.compile(r'(?i)oauth[_-]?token[\s]*[=:][\s]*[\'\"]?([a-zA-Z0-9]{16,64})[\'\"]?'),
            description="OAuth Token",
            risk_level="medium"
        ),

        # Slack
        SecretPattern(
            name="slack_token",
            pattern=re.compile(r'xox[baprs]-([0-9a-zA-Z]{10,48})'),
            description="Slack API Token",
            risk_level="high"
        ),

        # GitHub
        SecretPattern(
            name="github_token",
            pattern=re.compile(r'gh[pousr]_[A-Za-z0-9_]{36}'),
            description="GitHub Token",
            risk_level="high"
        ),

        # Email SMTP
        SecretPattern(
            name="smtp_password",
            pattern=re.compile(r'(?i)(smtp|email)[_-]?password[\s]*[=:][\s]*[\'\"]?([^\s\'\"]+)[\'\"]?'),
            description="SMTP/Email Password",
            risk_level="high"
        ),

        # Crypto Wallets
        SecretPattern(
            name="crypto_private_key",
            pattern=re.compile(r'[0-9a-fA-F]{64}'),
            description="Cryptocurrency Private Key",
            risk_level="critical"
        )
    ]
