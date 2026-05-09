import argparse
from osint.core import run_investigation

def main():
    parser = argparse.ArgumentParser(
        description="OSINT Toolkit — aggregates public intel on a target"
    )
    parser.add_argument("target", help="IP, domain, or email address")
    parser.add_argument("--type", choices=["ip", "domain", "email"],
                        required=True, help="Target type")
    parser.add_argument("--output", choices=["html", "json", "terminal"],
                        default="terminal")
    parser.add_argument("--modules", nargs="+",
                        help="Run specific modules only")
    args = parser.parse_args()

    run_investigation(args.target, args.type, args.output, args.modules)

if __name__ == "__main__":
    main()
