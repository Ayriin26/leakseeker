import os
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any, Generator, Set

from .filters import is_valid_secret
from .patterns import get_patterns
from .detectors import EntropyDetector


class SecretScanner:
    def __init__(self):
        self.patterns = get_patterns()
        self.entropy_detector = EntropyDetector()

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
        """Scan a file or directory for secrets"""
        results = []
        self._seen.clear()

        if path.is_file():
            results.extend(self.scan_file(path))
        else:
            for file_path in self.walk_directory(path):
                results.extend(self.scan_file(file_path))

        if scan_git_history and (path / '.git').exists():
            git_results = self.scan_git_history(path)
            results.extend(git_results)

        return results

    def walk_directory(self, directory: Path) -> Generator[Path, None, None]:
        """Walk through directory, skipping ignored paths"""
        for root, dirs, files in os.walk(directory):
            dirs[:] = [
                d for d in dirs
                if d not in self.ignored_dirs and not d.startswith('.')
            ]

            for file in files:
                file_path = Path(root) / file

                if (
                    file_path.suffix in self.supported_extensions
                    or file_path.name.startswith('.env')
                ):
                    yield file_path

    def scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Scan a single file for secrets"""
        results = []

        try:
            # Increased size limit
            if file_path.stat().st_size > 2_000_000:
                return results
        except OSError:
            return results

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:

                for line_num, line in enumerate(f, 1):

                    # Skip binary-like content
                    if '\x00' in line:
                        continue

                    line_lower = line.lower()

                    # Skip obvious test/dummy lines
                    if any(x in line_lower for x in ['test', 'example', 'dummy']):
                        continue

                    # =========================
                    # 🔍 Pattern-based detection
                    # =========================
                    for pattern in self.patterns:
                        for match in pattern.pattern.finditer(line):

                            if not self.is_valid_match(match, pattern.name):
                                continue

                            matched_text = self.extract_match_value(match)

                            dedup_key = (str(file_path), pattern.name, matched_text)
                            if dedup_key in self._seen:
                                continue

                            self._seen.add(dedup_key)

                            entropy = self.entropy_detector.shannon_entropy(matched_text)

                            confidence = min(
                                100,
                                int(entropy * 10 + len(set(matched_text)) * 2)
                            )

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

                    # =========================
                    # 🔍 Entropy-based detection
                    # =========================
                    entropy_matches = self.entropy_detector.detect_high_entropy(line)

                    for high_entropy_string in entropy_matches:

                        if not is_valid_secret(high_entropy_string):
                            continue

                        dedup_key = (str(file_path), 'high_entropy_string', high_entropy_string)

                        if dedup_key in self._seen:
                            continue

                        self._seen.add(dedup_key)

                        entropy = self.entropy_detector.shannon_entropy(high_entropy_string)

                        confidence = min(100, int(entropy * 12))

                        results.append({
                            'file': str(file_path),
                            'line_number': line_num,
                            'line_content': line.strip(),
                            'secret_type': 'high_entropy_string',
                            'description': 'High entropy string (possible secret)',
                            'risk_level': 'medium',
                            'confidence': confidence,
                            'matched_text': high_entropy_string,
                            'in_git_history': False
                        })

        except (PermissionError, IsADirectoryError):
            pass

        except Exception as e:
            print(f"Warning: failed to scan {file_path}: {e}", file=sys.stderr)

        return results

    def scan_git_history(self, repo_path: Path) -> List[Dict[str, Any]]:
        """Scan git history for secrets"""
        results = []

        try:
            result = subprocess.run(
                ['git', 'log', '--pretty=format:%H'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return results

            commit_hashes = result.stdout.strip().split('\n')

            for commit in commit_hashes[:50]:
                diff_result = subprocess.run(
                    ['git', 'show', commit],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=15
                )

                if diff_result.returncode != 0:
                    continue

                diff_content = diff_result.stdout

                for pattern in self.patterns:
                    for match in pattern.pattern.finditer(diff_content):

                        if not self.is_valid_match(match, pattern.name):
                            continue

                        matched_text = self.extract_match_value(match)

                        dedup_key = (f'git:{commit[:8]}', pattern.name, matched_text)
                        if dedup_key in self._seen:
                            continue

                        self._seen.add(dedup_key)

                        entropy = self.entropy_detector.shannon_entropy(matched_text)

                        confidence = min(100, int(entropy * 10))

                        results.append({
                            'file': f'git:{commit[:8]}',
                            'line_number': 0,
                            'line_content': 'Found in git history',
                            'secret_type': pattern.name,
                            'description': f'{pattern.description} (in git history)',
                            'risk_level': pattern.risk_level,
                            'confidence': confidence,
                            'matched_text': matched_text,
                            'in_git_history': True
                        })

        except subprocess.TimeoutExpired:
            return results
        except Exception:
            return results

        return results

    @staticmethod
    def extract_match_value(match: Any) -> str:
        """Extract best captured value"""
        groups = [g for g in match.groups() if g]
        if groups:
            return groups[-1].strip()
        return match.group().strip()

    def is_valid_match(self, match: Any, pattern_name: str) -> bool:
        matched_text = match.group()

        if self.is_false_positive(matched_text, pattern_name):
            return False

        return is_valid_secret(self.extract_match_value(match))

    @staticmethod
    def is_false_positive(matched_text: str, pattern_name: str) -> bool:
        """Filter out obvious false positives"""
        exact_fp = {
            'example', 'test', 'demo', 'sample', 'placeholder',
            'fake', '000000', '123456', 'abcdef', 'changeme'
        }

        lower = matched_text.lower()

        if lower in exact_fp:
            return True

        placeholder_markers = (
            '_placeholder', 'your_secret', 'your_key', 'changeme', 'xxxx', '<', '>'
        )

        if any(marker in lower for marker in placeholder_markers):
            return True

        return False