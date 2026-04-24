// api-client.js — Frontend API client
// ⚠️  DEMO FILE: Intentionally contains hardcoded secrets for leakseeker demo
// 🔴 These credentials are accidentally bundled into the client-side build

// ── Hardcoded API tokens (should NEVER be in frontend code) ──────
const STRIPE_PUBLIC_KEY = "pk_live_51Hh3YrKZ5q2eXaMpLePublicKeyABCDEFGHIJKLMNOPQRST";
const GOOGLE_MAPS_KEY   = "AIzaSyD-9tSrke72I6e9E8d7X3kY8mN0pQ2wR4v";
const FIREBASE_API_KEY  = "AIzaSyBxK9mP2qR7vZd3F1nL8oT5sY6wE0jaBcD";

// 🔴 Secret key accidentally left in frontend bundle
const STRIPE_SECRET_KEY = "sk_live_51Hh3YrKZ5q2eXaMpLeKeyAbcDeFgHiJkLmNoPqRsTuVwXyZ12";

const API_BASE     = "https://api.mycompany.com";
const INTERNAL_URL = "http://localhost:8080/api/v1";  // dev endpoint left in prod build
const ADMIN_URL    = "/admin/panel";                  // exposed path
const GRAPHQL_URL  = "/graphql/internal";

// Auth tokens hardcoded (e.g. copied from Postman and forgot to remove)
const AUTH_HEADER = {
  Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEyMywiZW1haWwiOiJhZG1pbkBteWNvbXBhbnkuY29tIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzA5MDAwMDAwfQ.xK9mP2qR7vZd3F1nL8oT5sY6wE0jaBcDeFgHiJkLmNo",
};

const GITHUB_TOKEN  = "ghp_R8xN3kPqZ7vT2mYwL9dF4jA6sQ1nE5oB0cI";
const SLACK_WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXX";

// OAuth
const OAUTH_TOKEN = "oauth_token=ya29.a0AfH6SMBxN3kPqZ7vT2mYwL9dF4jA6sQ1nE5oBcD";

// ── API client ───────────────────────────────────────────────────

async function fetchUsers() {
  const res = await fetch(`${API_BASE}/api/v1/users`, {
    headers: AUTH_HEADER,
  });
  return res.json();
}

async function fetchAdminData() {
  // 🔴 Calling internal/admin endpoint from client
  const res = await fetch(`${INTERNAL_URL}/internal/admin/users`, {
    headers: {
      Authorization: `Bearer ${GITHUB_TOKEN}`,
      "X-API-Key": GOOGLE_MAPS_KEY,
    },
  });
  return res.json();
}

async function chargeCard(token, amount) {
  // 🔴 Using secret key in the browser
  const res = await fetch("https://api.stripe.com/v1/charges", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${STRIPE_SECRET_KEY}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `amount=${amount}&currency=usd&source=${token}`,
  });
  return res.json();
}

async function sendSlackAlert(message) {
  return fetch(SLACK_WEBHOOK, {
    method: "POST",
    body: JSON.stringify({ text: message }),
  });
}

export { fetchUsers, fetchAdminData, chargeCard, sendSlackAlert };
