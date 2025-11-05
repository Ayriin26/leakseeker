import json
import csv
import sys
from typing import List, Dict, Any

try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama
    COLOR_AVAILABLE = True
except ImportError:
    COLOR_AVAILABLE = False

class TextReporter:
    def __init__(self, use_color=True):
        self.use_color = use_color and COLOR_AVAILABLE

    def report(self, results: List[Dict[str, Any]], verbose=False):
        if not results:
            print("✅ No secrets found!")
            return

        # Group by risk level
        critical = [r for r in results if r['risk_level'] == 'critical']
        high = [r for r in results if r['risk_level'] == 'high']
        medium = [r for r in results if r['risk_level'] == 'medium']
        low = [r for r in results if r['risk_level'] == 'low']

        print(f"\n🔍 Scan Results:")
        print(f"   Critical: {len(critical)}, High: {len(high)}, Medium: {len(medium)}, Low: {len(low)}")
        print(f"   Total: {len(results)} potential secrets found\n")

        for result in results:
            self.print_result(result, verbose)

    def print_result(self, result: Dict[str, Any], verbose: bool):
        risk_colors = {
            'critical': Fore.RED,
            'high': Fore.YELLOW,
            'medium': Fore.CYAN,
            'low': Fore.GREEN
        }

        color = risk_colors.get(result['risk_level'], '')
        reset = Style.RESET_ALL if self.use_color else ''

        # Risk indicator
        risk_indicator = "💀" if result['risk_level'] == 'critical' else "⚠️"

        print(f"{color}{risk_indicator} {result['risk_level'].upper()}: {result['description']}{reset}")
        print(f"   Type: {result['secret_type']}")
        print(f"   File: {result['file']}:{result['line_number']}")

        if result.get('in_git_history'):
            print(f"   📝 Found in Git History")

        if verbose:
            print(f"   Line: {result['line_content'][:100]}{'...' if len(result['line_content']) > 100 else ''}")

        print(f"   Match: {result['matched_text']}")
        print()

class JSONReporter:
    def report(self, results: List[Dict[str, Any]], verbose=False):
        print(json.dumps({
            'scan_results': results,
            'summary': {
                'total': len(results),
                'critical': len([r for r in results if r['risk_level'] == 'critical']),
                'high': len([r for r in results if r['risk_level'] == 'high']),
                'medium': len([r for r in results if r['risk_level'] == 'medium']),
                'low': len([r for r in results if r['risk_level'] == 'low'])
            }
        }, indent=2))

class CSVReporter:
    def report(self, results: List[Dict[str, Any]], verbose=False):
        if not results:
            return

        # Flatten results for CSV
        flat_results = []
        for result in results:
            flat_result = {
                'file': result['file'],
                'line_number': result['line_number'],
                'secret_type': result['secret_type'],
                'description': result['description'],
                'risk_level': result['risk_level'],
                'matched_text': result['matched_text'],
                'in_git_history': result.get('in_git_history', False)
            }
            flat_results.append(flat_result)

        writer = csv.DictWriter(sys.stdout, fieldnames=flat_results[0].keys())
        writer.writeheader()
        writer.writerows(flat_results)

def get_reporter(format_name: str, use_color=True):
    reporters = {
        'text': TextReporter,
        'json': JSONReporter,
        'csv': CSVReporter
    }
    reporter_class = reporters.get(format_name, TextReporter)
    return reporter_class(use_color=use_color)
