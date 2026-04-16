import json
import csv
import sys
from typing import List, Dict, Any
from leakseeker.ai_helper import generate_ai_explanation

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_AVAILABLE = True
except ImportError:
    COLOR_AVAILABLE = False


RISK_ICONS = {
    'critical': '💀',
    'high': '🔴',
    'medium': '🟡',
    'low': '🟢',
}

RISK_ORDER = ['critical', 'high', 'medium', 'low']


class TextReporter:
    def __init__(self, use_color=True):
        self.use_color = use_color and COLOR_AVAILABLE

    def report(self, results: List[Dict[str, Any]], verbose=False):
        if not results:
            print("✅ No secrets found!")
            return

        # Sort by risk → confidence
        results_sorted = sorted(
            results,
            key=lambda r: (
                RISK_ORDER.index(r.get('risk_level', 'low')),
                -r.get('confidence', 0)
            )
        )

        # Summary
        summary = {level: 0 for level in RISK_ORDER}
        for r in results:
            summary[r.get('risk_level', 'low')] += 1

        print("\n🔍 Scan Results Summary:")
        print(
            f"   Critical: {summary['critical']}, "
            f"High: {summary['high']}, "
            f"Medium: {summary['medium']}, "
            f"Low: {summary['low']}"
        )
        print(f"   Total: {len(results)} potential secrets found\n")

        for result in results_sorted:
            self.print_result(result, verbose)

    def print_result(self, result: Dict[str, Any], verbose: bool):
        if self.use_color:
            risk_colors = {
                'critical': Fore.RED,
                'high': Fore.YELLOW,
                'medium': Fore.CYAN,
                'low': Fore.GREEN
            }
            color = risk_colors.get(result.get('risk_level'), '')
            reset = Style.RESET_ALL
        else:
            color = reset = ''

        icon = RISK_ICONS.get(result.get('risk_level'), '⚠️')

        print(f"{color}{icon} {result.get('risk_level', '').upper()}{reset}")
        print(f"   Type       : {result.get('secret_type', '')}")
        print(f"   Location   : {result.get('file', '')}:{result.get('line_number', '')}")

        if result.get('in_git_history'):
            print("   📝 Found in Git History")

        # Confidence
        print(f"   Confidence : {result.get('confidence', 'N/A')}%")

        # Redacted match
        matched = result.get('matched_text', '')
        if len(matched) > 16:
            display = matched[:6] + '...' + matched[-4:]
        else:
            display = matched[:4] + '...'
        print(f"   Match      : {display}")

        if verbose:
            line = result.get('line_content', '')
            print(f"   Line       : {line[:120]}{'...' if len(line) > 120 else ''}")

        # AI Explanation
        ai_text = generate_ai_explanation(
            result.get("secret_type"),
            result.get("matched_text")
        )

        print("\n   🧠 Analysis:")
        for line in ai_text.split('\n'):
            print(f"   {line}")

        print("-" * 60)


class JSONReporter:
    def report(self, results: List[Dict[str, Any]], verbose=False):
        print(json.dumps({
            'scan_results': results,
            'summary': {
                'total': len(results),
                'critical': sum(1 for r in results if r.get('risk_level') == 'critical'),
                'high': sum(1 for r in results if r.get('risk_level') == 'high'),
                'medium': sum(1 for r in results if r.get('risk_level') == 'medium'),
                'low': sum(1 for r in results if r.get('risk_level') == 'low')
            }
        }, indent=2))


class CSVReporter:
    FIELDS = [
        'file', 'line_number', 'secret_type',
        'risk_level', 'confidence', 'matched_text', 'in_git_history'
    ]

    def report(self, results: List[Dict[str, Any]], verbose=False):
        if not results:
            return

        def redact(value: str) -> str:
            if not value:
                return ""
            if len(value) > 16:
                return value[:6] + "..." + value[-4:]
            return value[:4] + "..."

        safe_results = []
        for r in results:
            r_copy = r.copy()
            r_copy['matched_text'] = redact(r_copy.get('matched_text', ''))
            safe_results.append(r_copy)

        writer = csv.DictWriter(sys.stdout, fieldnames=self.FIELDS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(safe_results)


def get_reporter(format_name: str, use_color=True):
    if format_name == 'json':
        return JSONReporter()
    elif format_name == 'csv':
        return CSVReporter()
    return TextReporter(use_color=use_color)