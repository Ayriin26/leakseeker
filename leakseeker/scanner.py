import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Generator
from .patterns import get_patterns
from .detectors import EntropyDetector

class SecretScanner:
    def __init__(self):
        self.patterns = get_patterns()
        self.entropy_detector = EntropyDetector()
        self.ignored_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'vendor', 'dist', 'build'}
        self.supported_extensions = {
            '.py', '.js', '.java', '.php', '.rb', '.go', '.rs',
            '.cpp', '.c', '.h', '.html', '.xml', '.json', '.yml',
            '.yaml', '.env', '.config', '.txt', '.md', '.ts', '.jsx', '.tsx'
        }

    def scan(self, path: Path, scan_git_history: bool = False) -> List[Dict[str, Any]]:
        """Scan a file or directory for secrets"""
        results = []

        if path.is_file():
            results.extend(self.scan_file(path))
        else:
            for file_path in self.walk_directory(path):
                results.extend(self.scan_file(file_path))

        if scan_git_history and (path / '.git').exists():
            git_results = self.scan_git_history(path)
            for result in git_results:
                result['in_git_history'] = True
            results.extend(git_results)

        return results

    def walk_directory(self, directory: Path) -> Generator[Path, None, None]:
        """Walk through directory, skipping ignored paths"""
        for root, dirs, files in os.walk(directory):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs and not d.startswith('.')]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.supported_extensions or file_path.name.startswith('.env'):
                    yield file_path

    def scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Scan a single file for secrets"""
        results = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()

                for line_num, line in enumerate(lines, 1):
                    # Pattern-based detection
                    for pattern in self.patterns:
                        matches = pattern.pattern.finditer(line)
                        for match in matches:
                            # Skip obvious false positives
                            if self.is_false_positive(match.group(), pattern.name):
                                continue

                            results.append({
                                'file': str(file_path),
                                'line_number': line_num,
                                'line_content': line.strip(),
                                'secret_type': pattern.name,
                                'description': pattern.description,
                                'risk_level': pattern.risk_level,
                                'matched_text': match.group(),
                                'in_git_history': False
                            })

                    # Entropy-based detection
                    high_entropy_string = self.entropy_detector.detect_high_entropy(line)
                    if high_entropy_string:
                        results.append({
                            'file': str(file_path),
                            'line_number': line_num,
                            'line_content': line.strip(),
                            'secret_type': 'high_entropy_string',
                            'description': 'High entropy string (possible secret)',
                            'risk_level': 'medium',
                            'matched_text': high_entropy_string,
                            'in_git_history': False
                        })

        except Exception as e:
            # Skip files we can't read
            pass

        return results

    def scan_git_history(self, repo_path: Path) -> List[Dict[str, Any]]:
        """Scan git history for secrets that were committed and then removed"""
        try:
            # Get all commit hashes
            result = subprocess.run(
                ['git', 'log', '--pretty=format:%H'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return []

            commit_hashes = result.stdout.strip().split('\n')
            secrets_found = []

            for commit in commit_hashes[:50]:  # Limit to last 50 commits for performance
                # Get the diff for this commit
                diff_result = subprocess.run(
                    ['git', 'show', commit],
                    cwd=repo_path,
                    capture_output=True,
                    text=True
                )

                if diff_result.returncode == 0:
                    diff_content = diff_result.stdout
                    # Look for secrets in the diff (both additions and removals)
                    for pattern in self.patterns:
                        matches = pattern.pattern.finditer(diff_content)
                        for match in matches:
                            if not self.is_false_positive(match.group(), pattern.name):
                                secrets_found.append({
                                    'file': f'git:{commit[:8]}',
                                    'line_number': 0,
                                    'line_content': 'Found in git history',
                                    'secret_type': pattern.name,
                                    'description': f'{pattern.description} (in git history)',
                                    'risk_level': pattern.risk_level,
                                    'matched_text': match.group(),
                                    'in_git_history': True
                                })

            return secrets_found
        except Exception:
            return []

    def is_false_positive(self, matched_text: str, pattern_name: str) -> bool:
        """Filter out common false positives"""
        false_positives = {
            'example', 'test', 'demo', 'sample', 'placeholder', 'fake',
            '000000', '123456', 'abcdef', 'changeme'
        }

        # Check if it's obviously a test/example value
        if matched_text.lower() in false_positives:
            return True

        # Check for common example patterns
        if 'example' in matched_text.lower():
            return True

        return False
