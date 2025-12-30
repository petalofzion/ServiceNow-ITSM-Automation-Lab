"""Trigger ATF suites via CI/CD API and store results."""
from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ATF suites")
    parser.add_argument("--suite", required=True, help="ATF suite name")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"Triggering ATF suite: {args.suite}")


if __name__ == "__main__":
    main()
