"""Trigger ATF suites via ServiceNow ATF API and store results."""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ATF suites")
    parser.add_argument("--suite", help="ATF suite name (falls back to env or desired state)")
    return parser.parse_args()


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


def _request_json(url: str, method: str, headers: dict[str, str], body: dict | None = None) -> dict:
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, method=method, data=data)
    for key, value in headers.items():
        req.add_header(key, value)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def _basic_headers(username: str, password: str) -> dict[str, str]:
    token = f"{username}:{password}".encode("utf-8")
    auth = base64.b64encode(token).decode("ascii")
    return {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _resolve_suite_name(args: argparse.Namespace, env: dict[str, str]) -> str:
    if args.suite and args.suite.strip():
        return args.suite
    if env.get("SERVICENOW_ATF_SUITE"):
        return env["SERVICENOW_ATF_SUITE"]
    desired_state = Path("ops/desired-state/tests.yml")
    if desired_state.exists():
        data = yaml.safe_load(desired_state.read_text())
        suites = data.get("tests", {}).get("suites", [])
        if suites:
            return suites[0].get("name", "Smoke")
    return "Smoke"


def _lookup_suite_sys_id(instance: str, headers: dict[str, str], suite_name: str) -> str:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": f"name={suite_name}",
            "sysparm_fields": "sys_id,name",
            "sysparm_limit": "1",
        }
    )
    url = f"{instance}/api/now/table/sys_atf_test_suite?{query}"
    payload = _request_json(url, "GET", headers)
    results = payload.get("result", [])
    if not results:
        available = _list_suites(instance, headers)
        if available:
            names = ", ".join(item["name"] for item in available)
            raise SystemExit(f"ATF suite not found: {suite_name}. Available: {names}")
        raise SystemExit(f"ATF suite not found: {suite_name}. No suites found.")
    return results[0]["sys_id"]


def _list_suites(instance: str, headers: dict[str, str]) -> list[dict]:
    query = urllib.parse.urlencode(
        {
            "sysparm_fields": "sys_id,name",
            "sysparm_limit": "10",
            "sysparm_order_by": "name",
        }
    )
    url = f"{instance}/api/now/table/sys_atf_test_suite?{query}"
    payload = _request_json(url, "GET", headers)
    return payload.get("result", [])


def _suite_test_count(instance: str, headers: dict[str, str], suite_sys_id: str) -> int:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": f"test_suite={suite_sys_id}",
            "sysparm_limit": "1",
        }
    )
    url = f"{instance}/api/now/table/sys_atf_test_suite_test?{query}"
    payload = _request_json(url, "GET", headers)
    return len(payload.get("result", []))


def _trigger_suite(instance: str, headers: dict[str, str], suite_sys_id: str) -> dict:
    url = f"{instance}/api/sn_atf/run/suite/{suite_sys_id}"
    try:
        return _request_json(url, "POST", headers, body={})
    except urllib.error.HTTPError as exc:
        if exc.code == 400:
            raise SystemExit(
                "ATF run API endpoint is not available on this instance. "
                "Run the suite manually in the UI or enable the ATF run API plugin."
            ) from exc
        raise


def _latest_suite_result(instance: str, headers: dict[str, str], suite_sys_id: str) -> dict | None:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": f"test_suite={suite_sys_id}",
            "sysparm_fields": "sys_id,result,state,status,passed,failed,sys_created_on",
            "sysparm_limit": "1",
            "sysparm_order_by": "-sys_created_on",
        }
    )
    url = f"{instance}/api/now/table/sys_atf_test_suite_result?{query}"
    payload = _request_json(url, "GET", headers)
    results = payload.get("result", [])
    return results[0] if results else None


def _interpret_result(result: dict) -> str | None:
    for key in ("result", "state", "status"):
        value = result.get(key)
        if isinstance(value, str) and value:
            return value.lower()
    return None


def main() -> None:
    args = parse_args()
    env = _get_env()
    instance = env.get("SERVICENOW_INSTANCE_URL")
    username = env.get("SERVICENOW_USERNAME")
    password = env.get("SERVICENOW_PASSWORD")
    if not all([instance, username, password]):
        raise SystemExit("Missing ServiceNow credentials in tools/servicenow-mcp/.env")

    suite_name = _resolve_suite_name(args, env)
    headers = _basic_headers(username, password)

    print(f"Resolving ATF suite: {suite_name}")
    suite_sys_id = _lookup_suite_sys_id(instance.rstrip("/"), headers, suite_name)
    suite_tests = _suite_test_count(instance.rstrip("/"), headers, suite_sys_id)
    if suite_tests == 0:
        raise SystemExit(
            f"ATF suite '{suite_name}' has no tests. Create tests or attach existing ones before running."
        )
    print(f"Triggering ATF suite {suite_name} ({suite_sys_id})")
    response = _trigger_suite(instance.rstrip("/"), headers, suite_sys_id)
    print(f"ATF trigger response: {response}")

    print("Waiting for latest suite result...")
    deadline = time.time() + 600
    while time.time() < deadline:
        result = _latest_suite_result(instance.rstrip("/"), headers, suite_sys_id)
        if result:
            status = _interpret_result(result)
            if status in {"passed", "success", "complete", "completed"}:
                print(f"ATF suite result: {status}")
                return
            if status in {"failed", "error", "cancelled", "canceled"}:
                raise SystemExit(f"ATF suite result: {status}")
        time.sleep(10)

    raise SystemExit("Timed out waiting for ATF suite result")


if __name__ == "__main__":
    main()
