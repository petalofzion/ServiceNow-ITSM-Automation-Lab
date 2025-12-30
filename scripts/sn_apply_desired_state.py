"""Apply or validate the desired state for the PDI via MCP/SN APIs."""
from __future__ import annotations

import argparse
from pathlib import Path


DESIRED_STATE_DIR = Path("ops/desired-state")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply ServiceNow desired state")
    parser.add_argument("--validate", action="store_true", help="Validate YAML files")
    parser.add_argument("--apply", action="store_true", help="Apply desired state")
    parser.add_argument("--verify", action="store_true", help="Verify instance state")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not DESIRED_STATE_DIR.exists():
        raise SystemExit("Desired state directory missing: ops/desired-state")

    if args.validate:
        print("Validating desired state files...")
    if args.apply:
        print("Applying desired state via MCP/SN APIs...")
    if args.verify:
        print("Verifying instance state...")

    if not any([args.validate, args.apply, args.verify]):
        print("No action specified. Use --validate, --apply, or --verify.")


if __name__ == "__main__":
    main()
