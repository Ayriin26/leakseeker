"""
settings.py — Django production configuration
⚠️  DEMO FILE: Intentionally contains hardcoded secrets for leakseeker demo
"""

import os

# ── Core ─────────────────────────────────────────────────────────
DEBUG = True  # 🔴 Should be False in production
ALLOWED_HOSTS = ["*"]  # 🔴 Too permissive

SECRET_KEY = "django-insecure-8f42a73054b1749f8f58848be5e6502c5a4d9b7e3d6f1a9b4c2e0d8f"

# ── Database ─────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "app_production",
        "USER": "superadmin",
        "PASSWORD": "Tr0ub4dor&3SecretPass2024!",
        "HOST": "prod-postgres.mycompany.com",
        "PORT": "5432",
    },
    "analytics": {
        "ENGINE": "djongo",
        "NAME": "analytics",
        "CLIENT": {
            "host": "mongodb+srv://dbAdmin:xK9!mP2qR7vZ@cluster0.xyz.mongodb.net/analytics",
        },
    },
}

# ── Cache / Redis ─────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:R3d!sP@ssw0rd2024@redis.internal:6379/1",
    }
}

# ── AWS ──────────────────────────────────────────────────────────
AWS_ACCESS_KEY_ID     = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY1"
AWS_STORAGE_BUCKET_NAME = "mycompany-prod-media"
AWS_S3_REGION_NAME    = "us-east-1"

# ── Stripe ───────────────────────────────────────────────────────
STRIPE_SECRET_KEY        = "sk_live_51Hh3YrKZ5q2eXaMpLeKeyAbcDeFgHiJkLmNoPqRsTuVwXyZ12"
STRIPE_PUBLIC_KEY        = "pk_live_51Hh3YrKZ5q2eXaMpLePublicKeyABCDEFGHIJKLMNOPQRST"
STRIPE_WEBHOOK_SECRET    = "whsec_xK9mP2qR7vZd3F1nL8oT5sY6wE0jaBcDeFgHiJkL"

# ── Razorpay ─────────────────────────────────────────────────────
RAZORPAY_KEY_ID     = "rzp_live_9A3bKzXmPqT7vR"
RAZORPAY_KEY_SECRET = "rzp_live_xK9mP2qR7vZd3F1nL8oT"

# ── Google ────────────────────────────────────────────────────────
GOOGLE_API_KEY          = "AIzaSyD-9tSrke72I6e9E8d7X3kY8mN0pQ2wR4v"
GOOGLE_OAUTH_SECRET     = "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"
FIREBASE_ADMIN_CRED     = "firebase-adminsdk-xyz12-3f9d2a1b8c7e4d0f6a5b2c9"

# ── JWT ───────────────────────────────────────────────────────────
JWT_SECRET_KEY          = "8f42a73054b1749f8f58848be5e6502c5a4d9b7e3d6f1a9b4c2e0d8f7a1b3c5d"
JWT_REFRESH_SECRET_KEY  = "9a3b5c7d1e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4"

# ── GitHub ────────────────────────────────────────────────────────
GITHUB_ACCESS_TOKEN     = "ghp_R8xN3kPqZ7vT2mYwL9dF4jA6sQ1nE5oB0cI"
GITHUB_WEBHOOK_SECRET   = "github_webhook_xK9mP2qR7vZd3F1nL8oT5sY6wE0j"

# ── Slack ─────────────────────────────────────────────────────────
SLACK_BOT_TOKEN         = "xoxb-17653672481-19874698323-pdFZKVeTuq8kWZngrg3gEED0"
SLACK_SIGNING_SECRET    = "xoxs-17653672481-pdFZKVeTuq8kWZngrg3g"

# ── Email / SMTP ──────────────────────────────────────────────────
EMAIL_BACKEND           = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST              = "smtp.gmail.com"
EMAIL_PORT              = 587
EMAIL_HOST_USER         = "noreply@mycompany.com"
EMAIL_HOST_PASSWORD     = "EmailP@ssw0rd!2024Secure"
SENDGRID_API_KEY        = "SG.xK9mP2qR7vZd3F1nL8oT.5sY6wE0jaBcDeFgHiJkLmNoPqRsTuVwXyZ1234"

# ── OAuth ─────────────────────────────────────────────────────────
OAUTH_TOKEN             = "ya29.a0AfH6SMBxN3kPqZ7vT2mYwL9dF4jA6sQ1nE5oBcD"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "xK9mP2qR7vZd3F1nL8oT5sY6wE0jaBcDeFgH"

# ── Internal Service URLs ─────────────────────────────────────────
INTERNAL_API_URL        = "http://10.0.1.50:8080/internal/api/v1"
ADMIN_PANEL_URL         = "http://0.0.0.0:9000/admin"
DEBUG_ENDPOINT_URL      = "http://localhost:5000/debug/vars"
METRICS_URL             = "http://192.168.1.100:9090/metrics"
MANAGEMENT_API_URL      = "https://management.mycompany.com/internal/admin"

# ── Private Key ───────────────────────────────────────────────────
RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA2a2rwplBQLzJpKAHHcVEX/H96nbpNqsOGBMgKgWP6Lxz1Bb
gHRkJWAFm9dTK9/k9pjHg5l8Z8LkJ1nE5oBcDeFgHiJkLmNoPqRsTuVwXyZ1234
...
-----END RSA PRIVATE KEY-----"""

CRYPTO_PRIVATE_KEY = "private_key=a3f4b2c1e9d8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2"
