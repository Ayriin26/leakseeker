<div align="center">

```
██╗     ███████╗ █████╗ ██╗  ██╗███████╗███████╗███████╗██╗  ██╗███████╗██████╗ 
██║     ██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║     █████╗  ███████║█████╔╝ ███████╗█████╗  █████╗  █████╔╝ █████╗  ██████╔╝
██║     ██╔══╝  ██╔══██║██╔═██╗ ╚════██║██╔══╝  ██╔══╝  ██╔═██╗ ██╔══╝  ██╔══██╗
███████╗███████╗██║  ██║██║  ██╗███████║███████╗███████╗██║  ██╗███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
```

**Find hardcoded secrets before they find you.**

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE.txt)
[![Security](https://img.shields.io/badge/Purpose-Security-red?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/Ayriin26/leakseeker)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)](https://github.com/Ayriin26/leakseeker)

</div>

---

## 🔥 What is LeakSeeker?

LeakSeeker is a **fast, zero-dependency CLI tool** that hunts down hardcoded secrets, API keys, and credentials lurking in your codebase — before attackers do.

Whether it's an AWS key you forgot about, a Stripe secret left in a config file, or a JWT token buried in git history — LeakSeeker finds it.

---

## ⚡ Features

| Feature | Description |
|---|---|
| 🎯 **Pattern Detection** | 11+ built-in patterns for AWS, Stripe, GitHub, Slack, JWT, and more |
| 🧠 **Entropy Analysis** | Catches secrets that don't match any pattern using Shannon entropy |
| 📜 **Git History Scan** | Finds secrets in old commits — even ones that were "deleted" |
| 🎨 **Color-coded Output** | Risk levels highlighted: 💀 Critical, ⚠️ High, Medium, Low |
| 📊 **Multiple Formats** | Text, JSON, and CSV output |
| 🚀 **Fast** | Skips binaries, `node_modules`, `.git`, and other noise automatically |
| 🛡️ **False Positive Filtering** | Smart filtering to cut through placeholder and example values |

---

## 🚀 Installation

```bash
# Clone the repo
git clone https://github.com/Ayriin26/leakseeker.git
cd leakseeker

# Install
pip install -e .
```

---

## 🛠️ Usage

```bash
# Scan a project
leakseeker /path/to/your/project

# Verbose mode — shows the full line where the secret was found
leakseeker /path/to/project --verbose

# JSON output — great for piping into other tools
leakseeker /path/to/project --output json

# CSV output — save to a file for reporting
leakseeker /path/to/project --output csv > results.csv

# Also scan git history (finds deleted secrets too)
leakseeker /path/to/project --git-history

# No color (for CI environments)
leakseeker /path/to/project --no-color
```

---

## 🔍 What It Detects

```
💀 CRITICAL          ⚠️  HIGH              🔵 MEDIUM
─────────────────    ─────────────────    ─────────────────
AWS Access Keys      Database URLs        OAuth Tokens
AWS Secret Keys      JWT Secrets          High-entropy strings
Stripe API Keys      GitHub Tokens
Crypto Private Keys  Slack Tokens
                     SMTP Passwords
                     Generic API Keys
```

---

## 📸 Example Output

```
🔍 Scan Results:
   Critical: 2, High: 4, Medium: 2, Low: 0
   Total: 8 potential secrets found

💀 CRITICAL: AWS Secret Access Key
   Type: aws_secret_key
   File: config/settings.py:21
   Match: AWS_SECRET_ACCESS_KEY = 'wJalrXUtnFEMI/K7MDENG/...'

💀 CRITICAL: Stripe API Key
   Type: stripe_key
   File: config/settings.py:19
   Match: sk_live_51ABC123xyz789...

⚠️ HIGH: Database Connection URL with credentials
   Type: database_url
   File: .env:2
   Match: postgres://admin:password@localhost:5432/prod
```

---

## 🚦 Exit Codes

| Code | Meaning |
|---|---|
| `0` | ✅ Clean — no secrets found |
| `1` | ⚠️ Secrets found (low / medium / high risk) |
| `2` | 💀 Critical secrets found |
| `130` | Scan interrupted by user |

---

## 🗂️ Supported File Types

`.py` `.js` `.ts` `.jsx` `.tsx` `.java` `.php` `.rb` `.go` `.rs` `.cpp` `.c` `.h` `.html` `.xml` `.json` `.yml` `.yaml` `.env` `.config` `.txt` `.md`

> Files inside `node_modules`, `.git`, `__pycache__`, `dist`, `build`, and `vendor` are automatically skipped.

---

## 🤝 Contributing

Got a new secret pattern to add? Found a bug? PRs are welcome.

1. Fork the repo
2. Create a branch: `git checkout -b feature/new-pattern`
3. Add your pattern in `leakseeker/patterns.py`
4. Test it against `tests/test_data/`
5. Open a pull request

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<div align="center">

Made with 🔐 by [Ayriin26](https://github.com/Ayriin26)

*Don't leak secrets. Use LeakSeeker.*

</div>
