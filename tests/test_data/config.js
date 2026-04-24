// config.js — App configuration
// ⚠️  DEMO FILE: Intentionally contains hardcoded secrets for leakseeker demo

const config = {

  // ── App ────────────────────────────────────────────────────────
  app: {
    port: 3000,
    env: "production",
    secret: "n8vQx2KpR7mT4wZ9dF3jA6sL1cY5eG0hBiUoPlMnBv",
    baseUrl: "https://myapp.com",
  },

  // ── AWS ────────────────────────────────────────────────────────
  aws: {
    accessKeyId: "AKIAIOSFODNN7EXAMPLE",
    secretAccessKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY1",
    region: "us-east-1",
    s3Bucket: "mycompany-prod-assets",
  },

  // ── Stripe ─────────────────────────────────────────────────────
  stripe: {
    secretKey: "sk_live_51Hh3YrKZ5q2eXaMpLeKeyAbcDeFgHiJkLmNoPqRsTuVwXyZ12",
    publicKey: "pk_live_51Hh3YrKZ5q2eXaMpLePublicKeyABCDEFGHIJKLMNOPQRST",
    webhookSecret: "whsec_xK9mP2qR7vZd3F1nL8oT5sY6wE0jaBcDeFgH",
  },

  // ── Database ───────────────────────────────────────────────────
  database: {
    url: "postgresql://superadmin:Tr0ub4dor&3SecretPass@prod-postgres.mycompany.com:5432/app_production",
    mongo: "mongodb+srv://dbAdmin:xK9!mP2qR7vZ@cluster0.xyz.mongodb.net/prod",
    redis: "redis://:R3d!sP@ssw0rd2024@redis.internal:6379",
  },

  // ── JWT ────────────────────────────────────────────────────────
  jwt: {
    secret: "8f42a73054b1749f8f58848be5e6502c5a4d9b7e3d6f1a9b4c2e0d8f7a1b3c5d",
    refreshSecret: "9a3b5c7d1e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4",
    algorithm: "HS256",
    expiresIn: "7d",
  },

  // ── Google / Firebase ──────────────────────────────────────────
  google: {
    apiKey: "AIzaSyD-9tSrke72I6e9E8d7X3kY8mN0pQ2wR4v",
    clientSecret: "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",
    firebaseUrl: "https://myapp-12345.firebaseio.com/.json?auth=xK9mP2qR7vZd3",
  },

  // ── GitHub ─────────────────────────────────────────────────────
  github: {
    token: "ghp_R8xN3kPqZ7vT2mYwL9dF4jA6sQ1nE5oB0cI",
    oauthSecret: "3d9f2a1b8c7e4d0f6a5b2c9e8d7f4a1b3c5d2e",
  },

  // ── Slack ──────────────────────────────────────────────────────
  slack: {
    botToken: "xoxb-17653672481-19874698323-pdFZKVeTuq8kWZngrg3gEED0",
    signingSecret: "xoxs-17653672481-pdFZKVeTuq8kWZngrg3g",
    webhookUrl: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXX",
  },

  // ── Internal / Admin endpoints ─────────────────────────────────
  endpoints: {
    adminPanel:       "http://0.0.0.0:9000/admin/dashboard",
    debugVars:        "http://localhost:5000/debug/vars",
    internalMetrics:  "http://10.0.1.50:9090/metrics",
    internalApi:      "http://192.168.1.100:8080/internal/api/v1",
    managementApi:    "https://management.mycompany.com/internal/admin/users",
    privateReports:   "/private/reports/financials",
    graphqlInternal:  "/graphql/internal",
  },

  // ── SendGrid ───────────────────────────────────────────────────
  sendgrid: {
    apiKey: "SG.xK9mP2qR7vZd3F1nL8oT.5sY6wE0jaBcDeFgHiJkLmNoPqRsTuVwXyZ1234",
    smtpPassword: "EmailP@ssw0rd!2024Secure",
  },

  // ── OAuth ──────────────────────────────────────────────────────
  oauth: {
    token: "ya29.a0AfH6SMBxN3kPqZ7vT2mYwL9dF4jA6sQ1nE5oBcDeFgHi",
    clientSecret: "xK9mP2qR7vZd3F1nL8oT5sY6wE0jaBcDeFgH",
  },

};

module.exports = config;
