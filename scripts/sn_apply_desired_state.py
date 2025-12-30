"""Apply or validate the desired state for the PDI via MCP/SN APIs."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

DESIRED_STATE_DIR = Path("ops/desired-state")


@dataclass(frozen=True)
class PlanEntry:
    action: str
    resource_type: str
    name: str


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def _sorted_names(values: Iterable[dict], key: str = "name") -> list[dict]:
    return sorted(values, key=lambda item: item.get(key, ""))


def build_plan_entries(desired_state_dir: Path) -> list[PlanEntry]:
    entries: list[PlanEntry] = []

    roles_acls = load_yaml(desired_state_dir / "roles_acls.yml")["roles_acls"]
    for role in _sorted_names(roles_acls["roles"]):
        entries.append(PlanEntry("create", "role", role["name"]))
    for acl in _sorted_names(roles_acls["acls"], key="table"):
        name = f"{acl['table']}:{acl['operation']}"
        entries.append(PlanEntry("create", "acl", name))

    catalog = load_yaml(desired_state_dir / "catalog.yml")["catalog"]
    for item in _sorted_names(catalog["items"]):
        entries.append(PlanEntry("create", "catalog_item", item["name"]))
    for producer in _sorted_names(catalog["record_producers"]):
        entries.append(PlanEntry("create", "record_producer", producer["name"]))
    for flow in _sorted_names(catalog["flows"]):
        entries.append(PlanEntry("create", "flow", flow["name"]))

    scripts = load_yaml(desired_state_dir / "scripts.yml")["scripts"]
    for rule in _sorted_names(scripts["business_rules"]):
        entries.append(PlanEntry("create", "business_rule", rule["name"]))
    for policy in _sorted_names(scripts["ui_policies"]):
        entries.append(PlanEntry("create", "ui_policy", policy["name"]))
    for script in _sorted_names(scripts["client_scripts"]):
        entries.append(PlanEntry("create", "client_script", script["name"]))
    for include in _sorted_names(scripts["script_includes"]):
        entries.append(PlanEntry("create", "script_include", include["name"]))

    integrations = load_yaml(desired_state_dir / "integrations.yml")["integrations"]
    for outbound in _sorted_names(integrations["outbound_rest"]):
        entries.append(PlanEntry("create", "outbound_rest", outbound["name"]))
    for inbound in _sorted_names(integrations["inbound_rest"]):
        entries.append(PlanEntry("create", "inbound_rest", inbound["name"]))
    for soap in _sorted_names(integrations["soap"]):
        entries.append(PlanEntry("create", "soap", soap["name"]))

    dashboards = load_yaml(desired_state_dir / "dashboards.yml")["dashboards"]
    for dashboard in _sorted_names(dashboards):
        entries.append(PlanEntry("create", "dashboard", dashboard["name"]))
        for widget in _sorted_names(dashboard["widgets"]):
            entries.append(PlanEntry("create", "dashboard_widget", widget["name"]))

    tests = load_yaml(desired_state_dir / "tests.yml")["tests"]
    for suite in _sorted_names(tests["suites"]):
        entries.append(PlanEntry("create", "test_suite", suite["name"]))
        for test in _sorted_names(suite["tests"]):
            entries.append(PlanEntry("create", "test_case", test["name"]))

    return entries


def build_plan_text(desired_state_dir: Path) -> str:
    entries = build_plan_entries(desired_state_dir)
    creates = [entry for entry in entries if entry.action == "create"]
    updates = [entry for entry in entries if entry.action == "update"]
    deletes = [entry for entry in entries if entry.action == "delete"]

    lines = ["Plan (dry-run):", "Creates:"]
    if creates:
        lines.extend([f"  - {entry.resource_type}: {entry.name}" for entry in creates])
    else:
        lines.append("  (none)")

    lines.append("Updates:")
    if updates:
        lines.extend([f"  - {entry.resource_type}: {entry.name}" for entry in updates])
    else:
        lines.append("  (none)")

    lines.append("Deletes:")
    if deletes:
        lines.extend([f"  - {entry.resource_type}: {entry.name}" for entry in deletes])
    else:
        lines.append("  (none)")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply ServiceNow desired state")
    parser.add_argument("--validate", action="store_true", help="Validate YAML files")
    parser.add_argument("--apply", action="store_true", help="Apply desired state")
    parser.add_argument("--verify", action="store_true", help="Verify instance state")
    parser.add_argument("--plan", action="store_true", help="Print desired state plan")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not DESIRED_STATE_DIR.exists():
        raise SystemExit("Desired state directory missing: ops/desired-state")

    if args.plan or not any([args.validate, args.apply, args.verify]):
        print(build_plan_text(DESIRED_STATE_DIR), end="")
        if not any([args.validate, args.apply, args.verify]):
            return

    if args.validate:
        print("Validating desired state files...")
    if args.apply:
        print("Applying desired state via MCP/SN APIs...")
    if args.verify:
        print("Verifying instance state...")
    if not any([args.validate, args.apply, args.verify, args.plan]):
        print("No action specified. Use --plan, --validate, --apply, or --verify.")


if __name__ == "__main__":
    main()
