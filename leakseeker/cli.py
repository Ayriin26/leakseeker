#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description='LeakSeeker - Find hardcoded secrets in your codebase',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  leakseeker /path/to/your/project
  leakseeker /path/to/project --verbose --output json
  leakseeker /path/to/project --output csv > results.csv
  leakseeker /path/to/project --git-history --no-color
        '''
    )

    parser.add_argument('path', help='Directory or file to scan')
    parser.add_argument('--output', '-o',
                       choices=['text', 'json', 'csv'],
                       default='text',
                       help='Output format (default: text)')
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Verbose output with line content')
    parser.add_argument('--no-color',
                       action='store_true',
                       help='Disable colored output')
    parser.add_argument('--git-history',
                       action='store_true',
                       help='Scan git history for previous commits')
    parser.add_argument('--version',
                       action='version',
                       version='LeakSeeker 0.1.0')

    args = parser.parse_args()

    target_path = Path(args.path)
    if not target_path.exists():
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Import here to avoid circular imports
    from leakseeker.scanner import SecretScanner
    from leakseeker.reporters import get_reporter

    try:
        scanner = SecretScanner()
        results = scanner.scan(target_path, scan_git_history=args.git_history)

        reporter = get_reporter(args.output, use_color=not args.no_color)
        reporter.report(results, verbose=args.verbose)

        # Exit with error code if critical issues found
        critical_count = len([r for r in results if r['risk_level'] == 'critical'])
        if critical_count > 0:
            sys.exit(2)
        elif len(results) > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\nScan interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error during scan: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
