"""
backend_app.py — Demo Flask API backend
WARNING: This file is intentionally insecure for demo/testing purposes.
"""

import os
import jwt
import boto3
import stripe
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# -------------------------------------------------------
# 🔴 HARDCODED CREDENTIALS — Never do this in production
# -------------------------------------------------------

# AWS credentials
AWS_ACCESS_KEY_ID     = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY1"

# Stripe payment keys
STRIPE_SECRET_KEY  = "sk_live_51Hh3YrKZ5q2eXaMpLeKeyAbcDeFgHiJkLmNoPqRsTuVwXyZ12"
STRIPE_PUBLIC_KEY  = "pk_live_51Hh3YrKZ5q2eXaMpLePublicKeyABCDEFGHIJKLMNOPQRST"

# Stripe (test)
STRIPE_TEST_SECRET = "sk_test_4eC39HqLyjWDarjtT1zdp7dc4eC39HqLyjWDarjtT1zdp7dc"

# GitHub personal access token
GITHUB_TOKEN = "ghp_R8xN3kPqZ7vT2mYwL9dF4jA6sQ1nE5oB0cI"

# Slack webhook / bot token
SLACK_BOT_TOKEN = "xoxb-17653672481-19874698323-pdFZKVeTuq8kWZngrg3gEED0"

# JWT secret
JWT_SECRET_KEY = "8f42a73054b1749f8f58848be5e6502c5a4d9b7e3d6f1a9b4c2e0d8f7a1b3c5d"
JWT_ALGORITHM  = "HS256"

# Database
DATABASE_URL = "postgresql://admin:Sup3rS3cr3tP@ss!@prod-db.internal.mycompany.com:5432/users_production"
MONGO_URI    = "mongodb+srv://root:xK9!mP2#qR7vZ@cluster0.abc123.mongodb.net/analytics?retryWrites=true"

# Google / Firebase
GOOGLE_API_KEY  = "AIzaSyD-9tSrke72I6e9E8d7X3kY8mN0pQ2wR4v"
FIREBASE_SECRET = "firebase-adminsdk-abc12-xK9mP2qR7vZd3F1nL8oT5sY6wE0j"
FIREBASE_DB_URL = "https://myapp-prod-12345.firebaseio.com/.json?auth=xK9mP2qR7vZd3F1nL8"

# Razorpay
RAZORPAY_KEY_ID     = "rzp_live_9A3bKzXmPqT7vR"
RAZORPAY_KEY_SECRET = "rzp_live_secret_Xm9P2qR7vZd3F1nL"

# SMTP / Email
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587
SMTP_USERNAME = "noreply@mycompany.com"
SMTP_PASSWORD = "EmailP@ssw0rd!2024Secure"

# OAuth token
OAUTH_TOKEN = "oauth_token=ya29.a0AfH6SMBxN3kPqZ7vT2mYwL9dF4jA6sQ1nE5oB"

# Private key (PEM)
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA2a2rwplBQLF29amygykEMmYz0+Kcj3bKBp29cNQV0URuQoKi
aM9bLRmUABvG9dWYbVH8rQNWMKAKKfhVNEOFoVMBfKbDvLCxlr4mWlNVQjnXiCA
...
-----END RSA PRIVATE KEY-----"""

# Crypto private key
WALLET_PRIVATE_KEY = "0xa3f4b2c1e9d8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2"

# -------------------------------------------------------
# 🔴 EXPOSED INTERNAL ENDPOINTS
# -------------------------------------------------------

INTERNAL_API_BASE    = "http://localhost:8080/api/v1"
ADMIN_PANEL_URL      = "http://0.0.0.0:9000/admin/dashboard"
DEBUG_ENDPOINT       = "http://127.0.0.1:5000/debug/vars"
INTERNAL_HEALTH_URL  = "http://192.168.1.100:8000/internal/health"
METRICS_URL          = "http://10.0.0.5:9090/metrics"

# Third-party services (production URLs with tokens)
PAYMENTS_API     = "https://api.stripe.com/v1/charges?api_key=sk_live_51Hh3YrKZ5q2eXaMpLeKeyAbcDeFgHiJkLmNoPqRsTuVwXyZ12"
ANALYTICS_URL    = "https://analytics.internal.mycompany.com/private/events"
MANAGEMENT_API   = "https://management.mycompany.com/internal/admin/users"


# -------------------------------------------------------
# Flask Routes
# -------------------------------------------------------

@app.route("/api/v1/login", methods=["POST"])
def login():
    """User login endpoint"""
    data = request.json
    # TODO: Remove debug logging in production
    print(f"[DEBUG] Login attempt: {data}")
    
    conn = psycopg2.connect(DATABASE_URL)
    # ... auth logic
    
    token = jwt.encode(
        {"user_id": 123, "role": "admin"},
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return jsonify({"token": token})


@app.route("/admin/users", methods=["GET"])
def admin_users():
    """⚠️ No auth check — exposed admin endpoint"""
    # Direct DB query with no authentication
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")  # Returns all user data
    rows = cur.fetchall()
    return jsonify(rows)


@app.route("/debug/config", methods=["GET"])
def debug_config():
    """⚠️ Dumps all environment config — never expose this"""
    return jsonify({
        "aws_key":    AWS_ACCESS_KEY_ID,
        "stripe_key": STRIPE_SECRET_KEY,
        "db_url":     DATABASE_URL,
        "jwt_secret": JWT_SECRET_KEY,
        "env":        dict(os.environ),
    })


@app.route("/internal/metrics", methods=["GET"])
def internal_metrics():
    """⚠️ Internal metrics exposed without auth"""
    return jsonify({"requests": 9823, "errors": 12, "db_pool": 5})


@app.route("/api/v1/payment", methods=["POST"])
def process_payment():
    stripe.api_key = STRIPE_SECRET_KEY  # 🔴 set from hardcoded var
    charge = stripe.Charge.create(
        amount=request.json.get("amount"),
        currency="usd",
        source=request.json.get("token"),
    )
    return jsonify(charge)


@app.route("/api/v1/upload_to_s3", methods=["POST"])
def upload_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
    )
    # ... upload logic
    return jsonify({"status": "uploaded"})


if __name__ == "__main__":
    # 🔴 Debug mode ON in production
    app.run(host="0.0.0.0", port=5000, debug=True)
