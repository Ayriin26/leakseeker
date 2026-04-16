"""
Offline AI-style explanations for detected secrets.
No API key required — all knowledge is built in.
"""

_EXPLANATIONS = {
    "aws_access_key": (
        "This key identifies an AWS account. Paired with a secret key, "
        "an attacker can access cloud services, read/write S3 buckets, "
        "launch EC2 instances, and incur large bills.",
        "Rotate immediately in the AWS IAM console. Store in environment "
        "variables or AWS Secrets Manager. Never commit to source control."
    ),
    "aws_secret_key": (
        "This provides full programmatic access to AWS resources. Exposure "
        "can lead to data theft, crypto-mining abuse, or full infrastructure takeover.",
        "Revoke via AWS IAM → Security credentials → Delete. Rotate and store "
        "using environment variables or a secrets manager."
    ),
    "stripe_key": (
        "Stripe secret keys allow real financial transactions, refunds, and "
        "customer data access. A live key leak can cause direct monetary loss.",
        "Rotate in the Stripe Dashboard immediately. Use only on the server side. "
        "Use restricted keys with minimal permissions."
    ),
    "private_key": (
        "Private keys enable authentication and encryption. Exposure grants "
        "complete identity impersonation and can compromise TLS, SSH, or signing.",
        "Revoke and regenerate the key pair. Never store private keys in source "
        "code — use a secrets manager or hardware security module."
    ),
    "jwt_secret": (
        "JWT secrets sign authentication tokens. With this secret, an attacker "
        "can forge tokens and impersonate any user, including admins.",
        "Change the secret immediately (all current sessions will be invalidated). "
        "Store in environment variables with at least 256 bits of randomness."
    ),
    "database_url": (
        "Database URLs often embed credentials. Direct DB access allows data "
        "exfiltration, modification, or destruction.",
        "Move to a .env file excluded from source control. Use a secrets manager "
        "in production. Apply least-privilege DB user permissions."
    ),
    "github_token": (
        "GitHub tokens can read/write code, manage secrets, trigger workflows, "
        "and access private repositories.",
        "Revoke in GitHub → Settings → Developer settings → Personal access tokens. "
        "Use fine-grained tokens with minimal scopes."
    ),
    "google_api_key": (
        "Google API keys may allow billing abuse, data scraping, or access to "
        "Maps, Cloud, or Firebase services depending on restrictions.",
        "Restrict the key to specific APIs and IP ranges in Google Cloud Console. "
        "Rotate if unrestricted."
    ),
    "slack_token": (
        "Slack tokens allow reading channel messages, sending messages as a bot, "
        "and accessing workspace data.",
        "Revoke in Slack API → Your Apps. Use OAuth scopes with minimum permissions."
    ),
    "discord_token": (
        "Discord tokens allow full bot/account control including sending messages, "
        "joining servers, and reading DMs.",
        "Regenerate the token in the Discord Developer Portal immediately."
    ),
    "smtp_password": (
        "Email credentials can be abused to send phishing/spam at scale, "
        "bypassing spam filters since it originates from a legitimate account.",
        "Change the password immediately. Use app-specific passwords and "
        "enable 2FA on the email account."
    ),
    "razorpay_key": (
        "Razorpay keys can process payments and access transaction data.",
        "Rotate in the Razorpay Dashboard. Keep secret keys server-side only."
    ),
    "oauth_token": (
        "OAuth tokens grant delegated access on behalf of a user. Theft allows "
        "acting as that user within the token's scope.",
        "Revoke via the issuing service. Implement token expiry and refresh rotation."
    ),
    "bearer_token": (
        "Bearer tokens are credentials — whoever holds this token is authenticated.",
        "Treat like a password. Store securely and transmit only over HTTPS."
    ),
    "jwt_token": (
        "This is a live JWT token. If not expired, it can be used to authenticate "
        "to the API it was issued for.",
        "Ensure tokens have short expiry (e.g. 15 min). Rotate signing secrets."
    ),
    "crypto_private_key": (
        "A 64-character hex string is likely a cryptocurrency private key. "
        "Exposure means permanent loss of all associated funds.",
        "Transfer funds to a new wallet immediately. Never store crypto keys in code."
    ),
    "firebase_url": (
        "Firebase URLs expose your database endpoint. If rules are misconfigured, "
        "data may be publicly readable or writable.",
        "Audit Firebase Security Rules. Ensure read/write require authentication."
    ),
    "high_entropy_string": (
        "This string has high randomness and may be a secret token, key, or password.",
        "Review manually. If it is a secret, move to environment variables and "
        "remove from source code."
    ),
    "api_key": (
    "Generic API keys may grant access to services and data.",
    "Store securely and rotate if exposed."
    )
}

_DEFAULT = (
    "This value may expose sensitive information if publicly accessible.",
    "Move sensitive data to environment variables or a secrets manager."
)


def generate_ai_explanation(secret_type: str, value: str = "") -> str:
    """Return a risk description and remediation tip for the given secret type."""
    reason, fix = _EXPLANATIONS.get(secret_type, _DEFAULT)
    return f"Risk: {reason}\nFix : {fix}"
