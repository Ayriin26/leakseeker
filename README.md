# LeakSeeker 🔍

A CLI tool to find hardcoded secrets and API keys in your codebase.

## Features

- 🔍 **Pattern-based detection** for common secret types (AWS, Stripe, JWT, etc.)
- 🎯 **Entropy analysis** to detect random strings that could be secrets
- 📚 **Git history scanning** to find secrets in previous commits
- 🎨 **Colored output** with risk-level indicators
- 📊 **Multiple output formats** (text, JSON, CSV)
- ⚡ **Fast scanning** with intelligent file filtering

## Installation

```bash
# Install from source
git clone <repository>
cd leakseeker
pip install -e .

# Or install directly
pip install leakseeker
```

## Usage
```bash
# Basic scan
leakseeker /path/to/your/project

# Verbose output with JSON format
leakseeker /path/to/project --verbose --output json

# Scan including git history
leakseeker /path/to/project --git-history

# Save results to CSV
leakseeker /path/to/project --output csv > results.csv

# Disable colored output
leakseeker /path/to/project --no-color
```

## Supported Secret Types
- AWS Access Keys & Secret Keys
- Stripe API Keys
- Database Connection Strings
- JWT Secrets
- OAuth Tokens
- GitHub Tokens
- Slack API Tokens
- Generic API Keys
- SMTP Passwords
- High-entropy strings

## Exit Codes
- 0: No secrets found
- 1: Secrets found (low/medium/high risk)
- 2: Critical secrets found
- 130: User interrupted
- 1: Error during scan

## Contributing
1. Fork the repository
2. Create a feature branch
3. Add tests for new patterns
4. Submit a pull request

## License
MIT
