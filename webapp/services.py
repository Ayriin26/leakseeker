import tempfile
import zipfile
import shutil
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any

from leakseeker.scanner import SecretScanner

RISK_ORDER = ['low', 'medium', 'high', 'critical']


def run_scan(
    path: Path,
    scan_git_history: bool = False,
    min_risk: str = 'low'
) -> Dict[str, Any]:
    """Run a LeakSeeker scan and return structured results."""
    scanner = SecretScanner()
    raw = scanner.scan(path, scan_git_history=scan_git_history)

    min_idx = RISK_ORDER.index(min_risk)
    findings = [
        r for r in raw
        if RISK_ORDER.index(r.get('risk_level', 'low')) >= min_idx
    ]

    findings_sorted = sorted(
        findings,
        key=lambda r: (
            RISK_ORDER.index(r.get('risk_level', 'low')),
            -r.get('confidence', 0)
        )
    )

    summary = {level: 0 for level in RISK_ORDER}
    for r in findings:
        summary[r.get('risk_level', 'low')] += 1

    weights = {'critical': 10, 'high': 7, 'medium': 4, 'low': 1}
    risk_score = min(100, sum(weights.get(r.get('risk_level', 'low'), 1) for r in findings))

    return {
        'findings': findings_sorted,
        'summary': summary,
        'total': len(findings),
        'risk_score': risk_score,
    }


def extract_upload(uploaded_file) -> Path:
    """Save and optionally unzip an uploaded file to a temp dir. Returns path to scan."""
    tmp_dir = Path(tempfile.mkdtemp(prefix='leakseeker_'))
    filename = uploaded_file.filename

    dest = tmp_dir / filename
    uploaded_file.save(str(dest))

    if filename.endswith('.zip'):
        extract_dir = tmp_dir / 'extracted'
        extract_dir.mkdir()
        with zipfile.ZipFile(dest, 'r') as zf:
            zf.extractall(extract_dir)
        dest.unlink()
        return extract_dir

    return dest


def cleanup_temp(path: Path):
    """Remove temp directory after scan."""
    try:
        root = path if path.is_dir() else path.parent
        # Only remove if it's actually a temp dir we created
        if 'leakseeker_' in root.name or 'leakseeker_' in root.parent.name:
            shutil.rmtree(root, ignore_errors=True)
    except Exception:
        pass

def extract_uploads(uploaded_files) -> Path:
    """Save multiple uploaded files into a single temp directory for scanning."""
    tmp_dir = Path(tempfile.mkdtemp(prefix='leakseeker_'))

    for uploaded_file in uploaded_files:
        filename = uploaded_file.filename
        dest = tmp_dir / filename
        uploaded_file.save(str(dest))

        if filename.endswith('.zip'):
            extract_dir = tmp_dir / (filename + '_extracted')
            extract_dir.mkdir()
            try:
                with zipfile.ZipFile(dest, 'r') as zf:
                    zf.extractall(extract_dir)
                dest.unlink()
            except zipfile.BadZipFile:
                pass  # Leave the file as-is if not a valid zip

    return tmp_dir


def clone_github_repo(github_url: str) -> Path:
    """Clone a public GitHub repository to a temp dir for scanning."""
    # Validate it looks like a GitHub URL
    pattern = r'^https?://github\.com/[\w\-\.]+/[\w\-\.]+(?:\.git)?/?$'
    if not re.match(pattern, github_url):
        raise ValueError(
            "Invalid GitHub URL. Expected format: https://github.com/owner/repo"
        )

    # Normalise: strip trailing slash / .git
    clean_url = github_url.rstrip('/').removesuffix('.git')

    tmp_dir = Path(tempfile.mkdtemp(prefix='leakseeker_gh_'))

    try:
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', clean_url, str(tmp_dir / 'repo')],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            # Surface a friendly error for private/missing repos
            if 'Repository not found' in stderr or 'not found' in stderr.lower():
                raise ValueError("Repository not found or is private. Only public repos are supported.")
            raise RuntimeError(f"git clone failed: {stderr}")
    except FileNotFoundError:
        raise RuntimeError("git is not installed on this server.")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Cloning timed out. The repository may be too large.")

    return tmp_dir / 'repo'
