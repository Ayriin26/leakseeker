#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='LeakSeeker - Find hardcoded secrets in your codebase',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''\
Examples:
  leakseeker /path/to/project
  leakseeker /path/to/project --verbose
  leakseeker /path/to/project --output json
  leakseeker /path/to/project --output csv > results.csv
  leakseeker /path/to/project --output html
  leakseeker /path/to/project --git-history --no-color
        '''
    )

    parser.add_argument('path', help='Directory or file to scan')

    parser.add_argument('--output', '-o',
                        choices=['text', 'json', 'csv', 'html'],
                        default='text',
                        help='Output format (default: text)')

    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Show the full source line where the secret was found')

    parser.add_argument('--no-color',
                        action='store_true',
                        help='Disable colored terminal output')

    parser.add_argument('--git-history',
                        action='store_true',
                        help='Also scan git history (last 50 commits)')

    parser.add_argument('--min-risk',
                        choices=['low', 'medium', 'high', 'critical'],
                        default='low',
                        help='Only show findings at or above this risk level (default: low)')

    parser.add_argument('--version',
                        action='version',
                        version='LeakSeeker 1.0.0')

    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    if not target_path.exists():
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)

    from leakseeker.scanner import SecretScanner
    from leakseeker.reporters import get_reporter
    from leakseeker.html_reporter import generate_html_report

    risk_order = ['low', 'medium', 'high', 'critical']
    min_risk_idx = risk_order.index(args.min_risk)

    try:
        print(f"🔍 Scanning: {target_path}\n", file=sys.stderr)

        scanner = SecretScanner()
        results = scanner.scan(target_path, scan_git_history=args.git_history)

        # Safe filtering
        results = [
            r for r in results
            if risk_order.index(r.get('risk_level', 'low')) >= min_risk_idx
        ]

        if args.output == 'html':
            print("📄 Generating HTML report...", file=sys.stderr)
            generate_html_report(results)
        else:
            reporter = get_reporter(args.output, use_color=not args.no_color)
            reporter.report(results, verbose=args.verbose)

        critical_count = sum(1 for r in results if r['risk_level'] == 'critical')

        if critical_count > 0:
            sys.exit(2)
        elif results:
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\nScan interrupted by user", file=sys.stderr)
        sys.exit(130)

    except ImportError as e:
        print(f"Missing dependency: {e}", file=sys.stderr)
        print("Try installing required packages (e.g., matplotlib)", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Error during scan: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()