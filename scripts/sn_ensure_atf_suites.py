"""Ensure ATF suites exist and attach known tests by name when available."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import yaml

import base64
import os
import urllib.parse
import urllib.request


def _load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _get_env() -> dict[str, str]:
    env = dict(os.environ)
    env_path = Path("tools/servicenow-mcp/.env")
    env.update(_load_env_file(env_path))
    return env


def _basic_headers(username: str, password: str) -> dict[str, str]:
    token = f"{username}:{password}".encode("utf-8")
    auth = base64.b64encode(token).decode("ascii")
    return {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _request_json(url: str, method: str, headers: dict[str, str], body: dict | None = None) -> dict:
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, method=method, data=data)
    for key, value in headers.items():
        req.add_header(key, value)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


DESIRED_TESTS_PATH = Path("ops/desired-state/tests.yml")
OUTPUT_PATH = Path("artifacts/atf_suites.json")


def _load_desired_tests(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing desired tests file: {path}")
    return yaml.safe_load(path.read_text())


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _list_suites(instance: str, headers: dict[str, str]) -> list[dict]:
    url = f"{instance}/api/now/table/sys_atf_test_suite?sysparm_fields=sys_id,name"
    payload = _request_json(url, "GET", headers)
    return payload.get("result", [])


def _create_suite(instance: str, headers: dict[str, str], name: str) -> dict:
    url = f"{instance}/api/now/table/sys_atf_test_suite"
    body = {"name": name, "active": "true", "description": f"{name} suite (auto-managed)"}
    payload = _request_json(url, "POST", headers, body=body)
    return payload.get("result", {})


def _get_test_by_name(instance: str, headers: dict[str, str], name: str) -> dict | None:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": f"name={name}",
            "sysparm_fields": "sys_id,name",
            "sysparm_limit": "1",
        }
    )
    url = f"{instance}/api/now/table/sys_atf_test?{query}"
    payload = _request_json(url, "GET", headers)
    results = payload.get("result", [])
    return results[0] if results else None


def _suite_has_test(instance: str, headers: dict[str, str], suite_id: str, test_id: str) -> bool:
    url = (
        f"{instance}/api/now/table/sys_atf_test_suite_test?"
        f"sysparm_query=test_suite={suite_id}^test={test_id}&sysparm_limit=1"
    )
    payload = _request_json(url, "GET", headers)
    return bool(payload.get("result"))


def _add_test_to_suite(instance: str, headers: dict[str, str], suite_id: str, test_id: str) -> None:
    url = f"{instance}/api/now/table/sys_atf_test_suite_test"
    body = {"test_suite": suite_id, "test": test_id}
    _request_json(url, "POST", headers, body=body)


def _suite_map_by_name(suites: Iterable[dict]) -> dict[str, dict]:
    return {suite["name"]: suite for suite in suites if suite.get("name")}


def main() -> None:
    env = _get_env()
    instance = env.get("SERVICENOW_INSTANCE_URL")
    username = env.get("SERVICENOW_USERNAME")
    password = env.get("SERVICENOW_PASSWORD")
    if not all([instance, username, password]):
        raise SystemExit("Missing ServiceNow credentials in tools/servicenow-mcp/.env")

    instance = instance.rstrip("/")
    headers = _basic_headers(username, password)
    desired = _load_desired_tests(DESIRED_TESTS_PATH)

    suites = _list_suites(instance, headers)
    suites_by_name = _suite_map_by_name(suites)

    report: dict[str, dict] = {}

    for suite in desired.get("tests", {}).get("suites", []):
        suite_name = suite.get("name")
        if not suite_name:
            continue
        existing = suites_by_name.get(suite_name)
        if not existing:
            existing = _create_suite(instance, headers, suite_name)
            suites_by_name[suite_name] = existing
        suite_id = existing.get("sys_id")
        report[suite_name] = {"sys_id": suite_id, "tests": [], "missing_tests": []}

        for test in suite.get("tests", []):
            test_name = test.get("name")
            if not test_name or not suite_id:
                continue
            test_record = _get_test_by_name(instance, headers, test_name)
            if not test_record:
                report[suite_name]["missing_tests"].append(test_name)
                continue
            test_id = test_record.get("sys_id")
            if not test_id:
                continue
            if not _suite_has_test(instance, headers, suite_id, test_id):
                _add_test_to_suite(instance, headers, suite_id, test_id)
            report[suite_name]["tests"].append(test_name)

    _ensure_dir(OUTPUT_PATH)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2))

    print("ATF suites ensured.")
    for suite_name, details in report.items():
        missing = details.get("missing_tests", [])
        print(f"- {suite_name}: {details.get('sys_id')}")
        if missing:
            print(f"  Missing tests: {', '.join(missing)}")


if __name__ == "__main__":
    main()
