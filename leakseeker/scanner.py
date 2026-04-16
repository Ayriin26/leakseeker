import os
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any, Generator, Set

from .filters import is_valid_secret
from .patterns import get_patterns
from .detectors import EntropyDetector
from .endpoint_detector import EndpointDetector


class SecretScanner:
    def __init__(self):
        self.patterns = get_patterns()
        self.entropy_detector = EntropyDetector()
        self.endpoint_detector = EndpointDetector()

        self.ignored_dirs = {
            '.git', 'node_modules', '__pycache__', '.venv', 'venv',
            'vendor', 'dist', 'build', '.tox', '.mypy_cache', '.pytest_cache'
        }

        self.supported_extensions = {
            '.py', '.js', '.java', '.php', '.rb', '.go', '.rs',
            '.cpp', '.c', '.h', '.html', '.xml', '.json', '.yml',
            '.yaml', '.env', '.config', '.txt', '.md', '.ts', '.jsx', '.tsx',
            '.sh', '.bash', '.zsh', '.toml', '.ini', '.cfg', '.properties'
        }

        self._seen: Set[tuple] = set()

    def scan(self, path: Path, scan_git_history: bool = False) -> List[Dict[str, Any]]:
        results = []
        self._seen.clear()

        if path.is_file():
            results.extend(self.scan_file(path))
        else:
            for file_path in self.walk_directory(path):
                results.extend(self.scan_file(file_path))

        if scan_git_history and (path / '.git').exists():
            results.extend(self.scan_git_history(path))

        return results

    def walk_directory(self, directory: Path) -> Generator[Path, None, None]:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs and not d.startswith('.')]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.supported_extensions or file_path.name.startswith('.env'):
                    yield file_path

    def scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        results = []

        try:
            if file_path.stat().st_size > 2_000_000:
                return results
        except OSError:
            return results

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):

                    if '\x00' in line:
                        continue

                    # -------------------------
                    # Secret detection
                    # -------------------------
                    for pattern in self.patterns:
                        for match in pattern.pattern.finditer(line):

                            matched_text = self.extract_match_value(match)
                            lower_val = matched_text.lower()

                            if any(x in lower_val for x in ['test', 'example', 'dummy']):
                                continue

                            if not self.is_valid_match(match, pattern.name):
                                continue

                            dedup_key = (str(file_path), pattern.name, matched_text)
                            if dedup_key in self._seen:
                                continue

                            self._seen.add(dedup_key)

                            entropy = self.entropy_detector.shannon_entropy(matched_text)
                            confidence = min(100, int(entropy * 10 + len(set(matched_text)) * 2))

                            results.append({
                                'file': str(file_path),
                                'line_number': line_num,
                                'line_content': line.strip(),
                                'secret_type': pattern.name,
                                'description': pattern.description,
                                'risk_level': pattern.risk_level,
                                'confidence': confidence,
                                'matched_text': matched_text,
                                'in_git_history': False
                            })

                    # -------------------------
                    # Endpoint detection
                    # -------------------------
                    endpoints = self.endpoint_detector.detect(line)

                    confidence_map = {"high": 80, "medium": 60, "low": 40}

                    for ep in endpoints:
                        value = ep["value"]

                        dedup_key = (str(file_path), "endpoint", value)
                        if dedup_key in self._seen:
                            continue

                        self._seen.add(dedup_key)

                        results.append({
                            'file': str(file_path),
                            'line_number': line_num,
                            'line_content': line.strip(),
                            'secret_type': 'endpoint',
                            'description': 'Exposed web endpoint',
                            'risk_level': ep["risk"],
                            'confidence': confidence_map.get(ep["risk"], 50),
                            'matched_text': value,
                            'in_git_history': False
                        })

        except Exception as e:
            print(f"Warning: failed to scan {file_path}: {e}", file=sys.stderr)

        return results

    def scan_git_history(self, repo_path: Path) -> List[Dict[str, Any]]:
        results = []

        try:
            result = subprocess.run(
                ['git', 'log', '--pretty=format:%H'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return results

            commits = result.stdout.strip().split('\n')

            for commit in commits[:50]:
                diff = subprocess.run(
                    ['git', 'show', commit],
                    cwd=repo_path,
                    capture_output=True,
                    text=True
                )

                content = diff.stdout

                endpoints = self.endpoint_detector.detect(content)
                confidence_map = {"high": 80, "medium": 60, "low": 40}

                for ep in endpoints:
                    value = ep["value"]

                    dedup_key = (f'git:{commit[:8]}', 'endpoint', value)
                    if dedup_key in self._seen:
                        continue

                    self._seen.add(dedup_key)

                    results.append({
                        'file': f'git:{commit[:8]}',
                        'line_number': 0,
                        'line_content': 'Endpoint found in git history',
                        'secret_type': 'endpoint',
                        'description': 'Exposed endpoint (in git history)',
                        'risk_level': ep["risk"],
                        'confidence': confidence_map.get(ep["risk"], 50),
                        'matched_text': value,
                        'in_git_history': True
                    })

        except Exception:
            return results

        return results

    @staticmethod
    def extract_match_value(match: Any) -> str:
        groups = [g for g in match.groups() if g]
        return groups[-1].strip() if groups else match.group().strip()

    def is_valid_match(self, match: Any, pattern_name: str) -> bool:
        return is_valid_secret(self.extract_match_value(match))