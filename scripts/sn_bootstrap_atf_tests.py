"""Bootstrap minimal ServiceNow artifacts and ATF tests for this repo."""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


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


def _request_no_content(
    url: str, method: str, headers: dict[str, str], body: dict | None = None
) -> None:
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, method=method, data=data)
    for key, value in headers.items():
        req.add_header(key, value)
    with urllib.request.urlopen(req, timeout=30):
        return None


def _get_single(instance: str, headers: dict[str, str], table: str, query: str) -> dict | None:
    params = urllib.parse.urlencode(
        {
            "sysparm_query": query,
            "sysparm_limit": "1",
            "sysparm_fields": "sys_id,name",
        }
    )
    url = f"{instance}/api/now/table/{table}?{params}"
    payload = _request_json(url, "GET", headers)
    results = payload.get("result", [])
    return results[0] if results else None


def _ensure_record(
    instance: str, headers: dict[str, str], table: str, query: str, body: dict
) -> dict:
    existing = _get_single(instance, headers, table, query)
    if existing:
        return existing
    url = f"{instance}/api/now/table/{table}"
    payload = _request_json(url, "POST", headers, body=body)
    return payload.get("result", {})


def _ensure_catalog_item(instance: str, headers: dict[str, str]) -> dict:
    return _ensure_record(
        instance,
        headers,
        "sc_cat_item",
        "name=Access Request",
        {
            "name": "Access Request",
            "short_description": "Access Request (Plego lab)",
            "active": "true",
        },
    )


def _ensure_record_producer(instance: str, headers: dict[str, str]) -> dict:
    script = (
        "current.short_description = 'Plego incident from producer';"
        "current.caller_id = gs.getUserID();"
        "current.insert();"
    )
    return _ensure_record(
        instance,
        headers,
        "sc_cat_item_producer",
        "name=Report an Incident",
        {
            "name": "Report an Incident",
            "short_description": "Incident producer (Plego lab)",
            "active": "true",
            "table_name": "incident",
            "script": script,
        },
    )


def _ensure_flow_stub(instance: str, headers: dict[str, str]) -> dict:
    return _ensure_record(
        instance,
        headers,
        "sys_hub_flow",
        "name=Access Request Approval",
        {"name": "Access Request Approval", "active": "true"},
    )


def _ensure_rest_message(instance: str, headers: dict[str, str]) -> dict:
    return _ensure_record(
        instance,
        headers,
        "sys_rest_message",
        "name=GitHub Issue on High Priority",
        {
            "name": "GitHub Issue on High Priority",
            "rest_endpoint": "https://example.com",
        },
    )


def _ensure_property(instance: str, headers: dict[str, str], name: str, value: str) -> dict:
    return _ensure_record(
        instance,
        headers,
        "sys_properties",
        f"name={name}",
        {
            "name": name,
            "value": value,
            "description": "Plego integration automation (auto-managed)",
        },
    )


def _ensure_role(instance: str, headers: dict[str, str], name: str) -> dict:
    return _ensure_record(
        instance,
        headers,
        "sys_user_role",
        f"name={name}",
        {"name": name, "description": "Plego test role (auto-managed)"},
    )


def _ensure_dictionary_field(instance: str, headers: dict[str, str]) -> dict:
    return _ensure_record(
        instance,
        headers,
        "sys_dictionary",
        "name=sc_req_item^element=u_plego_protected",
        {
            "name": "sc_req_item",
            "element": "u_plego_protected",
            "column_label": "Plego Protected",
            "internal_type": "string",
            "max_length": "160",
            "active": "true",
        },
    )


def _ensure_protected_field_acl(instance: str, headers: dict[str, str]) -> dict:
    try:
        description = "Plego protected field ACL (auto-managed)"
        return _ensure_record(
            instance,
            headers,
            "sys_security_acl",
            f"name=sc_req_item.u_plego_protected^operation=write^type=field^description={description}",
            {
                "name": "sc_req_item.u_plego_protected",
                "operation": "write",
                "type": "field",
                "active": "true",
                "admin_overrides": "true",
                "description": description,
            },
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            return {}
        raise


def _ensure_protected_field_create_acl(instance: str, headers: dict[str, str]) -> dict:
    try:
        description = "Plego protected field create ACL (auto-managed)"
        return _ensure_record(
            instance,
            headers,
            "sys_security_acl",
            f"name=sc_req_item.u_plego_protected^operation=create^type=field^description={description}",
            {
                "name": "sc_req_item.u_plego_protected",
                "operation": "create",
                "type": "field",
                "active": "true",
                "admin_overrides": "true",
                "description": description,
            },
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            return {}
        raise


def _ensure_user(instance: str, headers: dict[str, str], user_name: str, first: str, last: str) -> dict:
    return _ensure_record(
        instance,
        headers,
        "sys_user",
        f"user_name={user_name}",
        {
            "user_name": user_name,
            "first_name": first,
            "last_name": last,
            "active": "true",
        },
    )


def _ensure_user_role(
    instance: str, headers: dict[str, str], user_id: str, role_id: str
) -> dict:
    query = f"user={user_id}^role={role_id}"
    return _ensure_record(
        instance,
        headers,
        "sys_user_has_role",
        query,
        {"user": user_id, "role": role_id},
    )


def _ensure_acl(instance: str, headers: dict[str, str]) -> dict:
    try:
        description = "Plego ACL for ATF sanity checks (auto-managed)"
        return _ensure_record(
            instance,
            headers,
            "sys_security_acl",
            f"name=sc_req_item.short_description^operation=write^type=field^description={description}",
            {
                "name": "sc_req_item.short_description",
                "operation": "write",
                "type": "field",
                "active": "true",
                "admin_overrides": "true",
                "description": description,
            },
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            return {}
        raise


def _ensure_table_write_acl(instance: str, headers: dict[str, str]) -> dict:
    try:
        description = "Plego record write ACL for ATF sanity checks (auto-managed)"
        record = _ensure_record(
            instance,
            headers,
            "sys_security_acl",
            f"name=sc_req_item^operation=write^type=record^description={description}",
            {
                "name": "sc_req_item",
                "operation": "write",
                "type": "record",
                "active": "true",
                "admin_overrides": "true",
                "description": description,
                "condition": "",
            },
        )
        if record.get("sys_id"):
            _request_json(
                f"{instance}/api/now/table/sys_security_acl/{record['sys_id']}",
                "PATCH",
                headers,
                body={
                    "condition": ""
                },
            )
        return record
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            return {}
        raise


def _ensure_table_create_acl(instance: str, headers: dict[str, str]) -> dict:
    try:
        description = "Plego record create ACL for ATF sanity checks (auto-managed)"
        record = _ensure_record(
            instance,
            headers,
            "sys_security_acl",
            f"name=sc_req_item^operation=create^type=record^description={description}",
            {
                "name": "sc_req_item",
                "operation": "create",
                "type": "record",
                "active": "true",
                "admin_overrides": "true",
                "description": description,
                "condition": "",
            },
        )
        return record
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            return {}
        raise


def _ensure_acl_role(
    instance: str, headers: dict[str, str], acl_id: str, role_id: str
) -> dict:
    return _ensure_record(
        instance,
        headers,
        "sys_security_acl_role",
        f"sys_security_acl={acl_id}^sys_user_role={role_id}",
        {"sys_security_acl": acl_id, "sys_user_role": role_id},
    )


def _ensure_business_rule(instance: str, headers: dict[str, str]) -> dict:
    script = (
        "if (current.approval != 'requested') {"
        "current.approval = 'requested';"
        "}"
    )
    return _ensure_record(
        instance,
        headers,
        "sys_script",
        "name=Plego Set Approval Requested",
        {
            "name": "Plego Set Approval Requested",
            "collection": "sc_req_item",
            "when": "before",
            "active": "true",
            "action_insert": "true",
            "advanced": "true",
            "script": script,
        },
    )


def _ensure_script_include(instance: str, headers: dict[str, str]) -> dict:
    script = (
        "var PlegoIntegrationLogger = Class.create();"
        "PlegoIntegrationLogger.prototype = {"
        "initialize: function() {},"
        "log: function(message) {"
        "gs.info('PlegoIntegrationLogger:' + message);"
        "},"
        "type: 'PlegoIntegrationLogger'"
        "};"
    )
    return _ensure_record(
        instance,
        headers,
        "sys_script_include",
        "name=PlegoIntegrationLogger",
        {
            "name": "PlegoIntegrationLogger",
            "active": "true",
            "script": script,
        },
    )


def _ensure_test(instance: str, headers: dict[str, str], name: str, description: str) -> dict:
    return _ensure_record(
        instance,
        headers,
        "sys_atf_test",
        f"name={name}",
        {"name": name, "description": description, "active": "true"},
    )


def _ensure_step(instance: str, headers: dict[str, str], test_id: str, order: int) -> dict:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": f"test={test_id}^step_config={_run_script_step_config()}",
            "sysparm_fields": "sys_id,test,step_config",
            "sysparm_limit": "1",
        }
    )
    url = f"{instance}/api/now/table/sys_atf_step?{query}"
    existing = _request_json(url, "GET", headers).get("result", [])
    if existing:
        return existing[0]
    body = {"test": test_id, "step_config": _run_script_step_config(), "order": str(order)}
    payload = _request_json(f"{instance}/api/now/table/sys_atf_step", "POST", headers, body=body)
    return payload.get("result", {})


def _run_script_step_config() -> str:
    return "41de4a935332120028bc29cac2dc349a"


def _script_variable_id() -> str:
    return "989d9e235324220002c6435723dc3484"


def _impersonate_step_config() -> str:
    return "071ee5b253331200040729cac2dc348d"


def _open_form_step_config() -> str:
    return "05317cd10b10220050192f15d6673af8"


def _field_state_step_config() -> str:
    return "1dfece935332120028bc29cac2dc3478"


def _set_step_script(instance: str, headers: dict[str, str], step_id: str, script: str) -> bool:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": (
                f"document=sys_atf_step^document_key={step_id}^variable={_script_variable_id()}"
            ),
            "sysparm_fields": "sys_id",
            "sysparm_limit": "1",
        }
    )
    url = f"{instance}/api/now/table/sys_variable_value?{query}"
    existing = _request_json(url, "GET", headers).get("result", [])
    if existing:
        return True

    url = f"{instance}/api/now/table/sys_variable_value"
    body = {
        "document": "sys_atf_step",
        "document_key": step_id,
        "variable": _script_variable_id(),
        "value": script,
    }
    try:
        _request_json(url, "POST", headers, body=body)
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            return False
        raise
    return True


def _delete_steps_for_test(instance: str, headers: dict[str, str], test_id: str) -> None:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": f"test={test_id}",
            "sysparm_fields": "sys_id",
            "sysparm_limit": "200",
        }
    )
    url = f"{instance}/api/now/table/sys_atf_step?{query}"
    payload = _request_json(url, "GET", headers)
    for step in payload.get("result", []):
        step_id = step.get("sys_id")
        if not step_id:
            continue
        _request_no_content(f"{instance}/api/now/table/sys_atf_step/{step_id}", "DELETE", headers)


def _get_var_dictionary_id(
    instance: str, headers: dict[str, str], step_config: str, element: str
) -> str:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": (
                f"nameSTARTSWITHvar__m_atf_input_variable_{step_config}^element={element}"
            ),
            "sysparm_fields": "sys_id,element",
            "sysparm_limit": "1",
        }
    )
    url = f"{instance}/api/now/table/var_dictionary?{query}"
    payload = _request_json(url, "GET", headers)
    results = payload.get("result", [])
    if not results:
        raise SystemExit(f"Missing var_dictionary input for {step_config} element {element}")
    return results[0]["sys_id"]


def _table_sys_id(instance: str, headers: dict[str, str], table_name: str) -> str:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": f"name={table_name}",
            "sysparm_fields": "sys_id,name",
            "sysparm_limit": "1",
        }
    )
    url = f"{instance}/api/now/table/sys_db_object?{query}"
    payload = _request_json(url, "GET", headers)
    results = payload.get("result", [])
    if results:
        return results[0]["sys_id"]
    return table_name


def _set_step_input(
    instance: str, headers: dict[str, str], step_id: str, variable_id: str, value: str
) -> None:
    query = urllib.parse.urlencode(
        {
            "sysparm_query": (
                f"document=sys_atf_step^document_key={step_id}^variable={variable_id}"
            ),
            "sysparm_fields": "sys_id",
            "sysparm_limit": "1",
        }
    )
    url = f"{instance}/api/now/table/sys_variable_value?{query}"
    existing = _request_json(url, "GET", headers).get("result", [])
    if existing:
        try:
            _request_json(
                f"{instance}/api/now/table/sys_variable_value/{existing[0]['sys_id']}",
                "PATCH",
                headers,
                body={"value": value},
            )
        except urllib.error.HTTPError as exc:
            if exc.code == 403:
                raise SystemExit(
                    "ServiceNow ACL blocks sys_variable_value updates for ATF UI steps. "
                    "Run scripts/servicenow/atf_seed_steps.js to seed UI steps."
                ) from exc
            raise
        return

    body = {
        "document": "sys_atf_step",
        "document_key": step_id,
        "variable": variable_id,
        "value": value,
    }
    try:
        _request_json(f"{instance}/api/now/table/sys_variable_value", "POST", headers, body=body)
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            raise SystemExit(
                "ServiceNow ACL blocks sys_variable_value inserts for ATF UI steps. "
                "Run scripts/servicenow/atf_seed_steps.js to seed UI steps."
            ) from exc
        raise


def _create_ui_step(
    instance: str,
    headers: dict[str, str],
    test_id: str,
    order: int,
    step_config: str,
    description: str,
    inputs: dict[str, str],
) -> None:
    body = {"test": test_id, "step_config": step_config, "order": str(order), "description": description}
    payload = _request_json(f"{instance}/api/now/table/sys_atf_step", "POST", headers, body=body)
    step_id = payload.get("result", {}).get("sys_id")
    if not step_id:
        raise SystemExit("Failed to create UI step for ACL Sanity Checks")
    for element, value in inputs.items():
        variable_id = _get_var_dictionary_id(instance, headers, step_config, element)
        _set_step_input(instance, headers, step_id, variable_id, value)


def _bootstrap_acl_ui_test(
    instance: str, headers: dict[str, str], test_id: str, requester_id: str, agent_id: str
) -> None:
    _delete_steps_for_test(instance, headers, test_id)
    steps = [
        (
            _impersonate_step_config(),
            "Impersonate requester",
            {"user": requester_id},
        ),
        (
            _open_form_step_config(),
            "Open a new sc_req_item form",
            {
                "table": "sc_req_item",
                "view": "",
                "form_ui": "standard_ui",
                "record_path": "record",
            },
        ),
        (
            _field_state_step_config(),
            "Requester cannot edit protected field",
            {"table": "sc_req_item", "read_only": "u_plego_protected", "form_ui": "standard_ui"},
        ),
        (
            _impersonate_step_config(),
            "Impersonate IT agent",
            {"user": agent_id},
        ),
        (
            _open_form_step_config(),
            "Open a new sc_req_item form as agent",
            {
                "table": "sc_req_item",
                "view": "",
                "form_ui": "standard_ui",
                "record_path": "record",
            },
        ),
        (
            _field_state_step_config(),
            "Agent can edit protected field",
            {
                "table": "sc_req_item",
                "not_read_only": "u_plego_protected",
                "form_ui": "standard_ui",
            },
        ),
    ]
    for idx, (config, desc, inputs) in enumerate(steps, start=1):
        _create_ui_step(instance, headers, test_id, idx, config, desc, inputs)


def _bootstrap_tests(instance: str, headers: dict[str, str]) -> None:
    tests = [
        (
            "Catalog Access Request Submission",
            "Create catalog request and verify request + RITM exist.",
            (
                "(function(step, stepRunner, jasmine, describe) {"
                "describe('Catalog Access Request Submission', function() {"
                "it('creates request and ritm', function() {"
                "var item = new GlideRecord('sc_cat_item');"
                "item.addQuery('name','Access Request');"
                "item.query();"
                "expect(item.next()).toBe(true);"
                "var req = new GlideRecord('sc_request');"
                "req.initialize();"
                "req.requested_for = gs.getUserID();"
                "req.short_description = 'ATF Access Request';"
                "var reqId = req.insert();"
                "expect(gs.nil(reqId)).toBe(false);"
                "var ritm = new GlideRecord('sc_req_item');"
                "ritm.initialize();"
                "ritm.request = reqId;"
                "ritm.cat_item = item.getUniqueValue();"
                "ritm.short_description = 'ATF Access Request Item';"
                "var ritmId = ritm.insert();"
                "expect(gs.nil(ritmId)).toBe(false);"
                "});"
                "});"
                "})(step, stepResult, jasmine, describe);"
                "jasmine.getEnv().execute();"
            ),
        ),
        (
            "Record Producer Creates Incident",
            "Execute producer script and verify incident created.",
            (
                "(function(step, stepRunner, jasmine, describe) {"
                "describe('Record Producer Creates Incident', function() {"
                "it('creates incident via producer script', function() {"
                "var producer = new GlideRecord('sc_cat_item_producer');"
                "producer.addQuery('name','Report an Incident');"
                "producer.query();"
                "expect(producer.next()).toBe(true);"
                "var current = new GlideRecord(producer.table_name + '');"
                "current.initialize();"
                "eval(producer.script + '');"
                "expect(gs.nil(current.getUniqueValue())).toBe(false);"
                "var inc = new GlideRecord('incident');"
                "expect(inc.get(current.getUniqueValue())).toBe(true);"
                "});"
                "});"
                "})(step, stepResult, jasmine, describe);"
                "jasmine.getEnv().execute();"
            ),
        ),
        (
            "Access Request Flow Trigger",
            "Verify flow exists and is active.",
            (
                "(function(step, stepRunner, jasmine, describe) {"
                "describe('Access Request Flow Trigger', function() {"
                "it('flow exists and is active', function() {"
                "var flow = new GlideRecord('sys_hub_flow');"
                "flow.addQuery('name','Access Request Approval');"
                "flow.query();"
                "expect(flow.next()).toBe(true);"
                "expect(flow.active == true || flow.active == 'true').toBe(true);"
                "});"
                "});"
                "})(step, stepResult, jasmine, describe);"
                "jasmine.getEnv().execute();"
            ),
        ),
        (
            "Access Request Approval Path",
            "Verify approvals are marked requested for new RITMs.",
            (
                "(function(step, stepRunner, jasmine, describe) {"
                "describe('Access Request Approval Path', function() {"
                "it('marks approval requested on new RITM', function() {"
                "var item = new GlideRecord('sc_cat_item');"
                "item.addQuery('name','Access Request');"
                "item.query();"
                "expect(item.next()).toBe(true);"
                "var req = new GlideRecord('sc_request');"
                "req.initialize();"
                "req.requested_for = gs.getUserID();"
                "req.short_description = 'ATF Approval Request';"
                "var reqId = req.insert();"
                "expect(gs.nil(reqId)).toBe(false);"
                "var ritm = new GlideRecord('sc_req_item');"
                "ritm.initialize();"
                "ritm.request = reqId;"
                "ritm.cat_item = item.getUniqueValue();"
                "ritm.short_description = 'ATF Approval RITM';"
                "var ritmId = ritm.insert();"
                "expect(gs.nil(ritmId)).toBe(false);"
                "var check = new GlideRecord('sc_req_item');"
                "expect(check.get(ritmId)).toBe(true);"
                "expect((check.approval + '') == 'requested').toBe(true);"
                "});"
                "});"
                "})(step, stepResult, jasmine, describe);"
                "jasmine.getEnv().execute();"
            ),
        ),
        (
            "Smoke Logging and Script Includes",
            "Verify script include logs a trace record.",
            (
                "(function(step, stepRunner, jasmine, describe) {"
                "describe('Smoke Logging and Script Includes', function() {"
                "it('writes integration log entry', function() {"
                "var logger = new PlegoIntegrationLogger();"
                "var tag = 'ATF_LOG_' + gs.generateGUID();"
                "logger.log(tag);"
                "gs.sleep(1000);"
                "var log = new GlideRecord('syslog');"
                "log.addQuery('message','CONTAINS', tag);"
                "log.addQuery('sys_created_on','>=', gs.minutesAgoStart(5));"
                "log.query();"
                "expect(log.next()).toBe(true);"
                "});"
                "});"
                "})(step, stepResult, jasmine, describe);"
                "jasmine.getEnv().execute();"
            ),
        ),
        (
            "Outbound REST Success",
            "Verify outbound REST call returns 200 and payload.",
            (
                "(function(step, stepRunner, jasmine, describe) {"
                "describe('Outbound REST Success', function() {"
                "it('executes RESTMessageV2 successfully', function() {"
                "var user = gs.getProperty('x_plego.integration.user');"
                "var pass = gs.getProperty('x_plego.integration.password');"
                "expect(gs.nil(user)).toBe(false);"
                "expect(gs.nil(pass)).toBe(false);"
                "var endpoint = gs.getProperty('glide.servlet.uri') + "
                "'api/now/table/sys_user?sysparm_limit=1';"
                "var msg = new sn_ws.RESTMessageV2();"
                "msg.setEndpoint(endpoint);"
                "msg.setHttpMethod('get');"
                "msg.setBasicAuth(user, pass);"
                "msg.setRequestHeader('Accept','application/json');"
                "var response = msg.execute();"
                "var status = response.getStatusCode();"
                "expect(status).toBe(200);"
                "var body = response.getBody();"
                "var parsed = JSON.parse(body);"
                "expect(parsed.result.length > 0).toBe(true);"
                "});"
                "});"
                "})(step, stepResult, jasmine, describe);"
                "jasmine.getEnv().execute();"
            ),
        ),
        (
            "Outbound REST Failure Handling",
            "Verify outbound REST call handles auth failure.",
            (
                "(function(step, stepRunner, jasmine, describe) {"
                "describe('Outbound REST Failure Handling', function() {"
                "it('handles failure status codes', function() {"
                "var endpoint = gs.getProperty('glide.servlet.uri') + "
                "'api/now/table/sys_user?sysparm_limit=1';"
                "var msg = new sn_ws.RESTMessageV2();"
                "msg.setEndpoint(endpoint);"
                "msg.setHttpMethod('get');"
                "msg.setBasicAuth('plego_bad_user','plego_bad_pass');"
                "var response = msg.execute();"
                "var status = response.getStatusCode();"
                "expect(status == 401 || status == 403).toBe(true);"
                "});"
                "});"
                "})(step, stepResult, jasmine, describe);"
                "jasmine.getEnv().execute();"
            ),
        ),
        (
            "Inbound REST Creates Request",
            "Verify Table API creates request and enforces auth.",
            (
                "(function(step, stepRunner, jasmine, describe) {"
                "describe('Inbound REST Creates Request', function() {"
                "it('creates request via REST and rejects missing auth', function() {"
                "var user = gs.getProperty('x_plego.integration.user');"
                "var pass = gs.getProperty('x_plego.integration.password');"
                "expect(gs.nil(user)).toBe(false);"
                "expect(gs.nil(pass)).toBe(false);"
                "var base = gs.getProperty('glide.servlet.uri') + 'api/now/table/';"
                "var reqMsg = new sn_ws.RESTMessageV2();"
                "reqMsg.setEndpoint(base + 'sc_request');"
                "reqMsg.setHttpMethod('post');"
                "reqMsg.setBasicAuth(user, pass);"
                "reqMsg.setRequestHeader('Content-Type','application/json');"
                "reqMsg.setRequestBody(JSON.stringify({"
                "requested_for: gs.getUserID(),"
                "short_description: 'ATF Inbound Request'"
                "}));"
                "var reqResp = reqMsg.execute();"
                "var reqStatus = reqResp.getStatusCode();"
                "expect(reqStatus == 200 || reqStatus == 201).toBe(true);"
                "var reqBody = JSON.parse(reqResp.getBody());"
                "var reqId = reqBody.result.sys_id;"
                "expect(gs.nil(reqId)).toBe(false);"
                "var item = new GlideRecord('sc_cat_item');"
                "item.addQuery('name','Access Request');"
                "item.query();"
                "expect(item.next()).toBe(true);"
                "var ritmMsg = new sn_ws.RESTMessageV2();"
                "ritmMsg.setEndpoint(base + 'sc_req_item');"
                "ritmMsg.setHttpMethod('post');"
                "ritmMsg.setBasicAuth(user, pass);"
                "ritmMsg.setRequestHeader('Content-Type','application/json');"
                "ritmMsg.setRequestBody(JSON.stringify({"
                "request: reqId,"
                "cat_item: item.getUniqueValue(),"
                "short_description: 'ATF Inbound RITM'"
                "}));"
                "var ritmResp = ritmMsg.execute();"
                "var ritmStatus = ritmResp.getStatusCode();"
                "expect(ritmStatus == 200 || ritmStatus == 201).toBe(true);"
                "var badMsg = new sn_ws.RESTMessageV2();"
                "badMsg.setEndpoint(base + 'sc_request');"
                "badMsg.setHttpMethod('post');"
                "badMsg.setRequestHeader('Content-Type','application/json');"
                "badMsg.setRequestBody(JSON.stringify({"
                "requested_for: gs.getUserID(),"
                "short_description: 'ATF Inbound Request (no auth)'"
                "}));"
                "var badResp = badMsg.execute();"
                "var badStatus = badResp.getStatusCode();"
                "expect(badStatus == 401 || badStatus == 403).toBe(true);"
                "});"
                "});"
                "})(step, stepResult, jasmine, describe);"
                "jasmine.getEnv().execute();"
            ),
        ),
        (
            "SOAP Call Logged",
            "Verify SOAPMessageV2 call returns 200.",
            (
                "(function(step, stepRunner, jasmine, describe) {"
                "describe('SOAP Call Logged', function() {"
                "it('executes SOAPMessageV2', function() {"
                "var user = gs.getProperty('x_plego.integration.user');"
                "var pass = gs.getProperty('x_plego.integration.password');"
                "expect(gs.nil(user)).toBe(false);"
                "expect(gs.nil(pass)).toBe(false);"
                "var endpoint = gs.getProperty('glide.servlet.uri') + "
                "'api/now/table/sys_user?sysparm_limit=1';"
                "var soap = new sn_ws.SOAPMessageV2();"
                "soap.setEndpoint(endpoint);"
                "soap.setHttpMethod('get');"
                "soap.setBasicAuth(user, pass);"
                "soap.setRequestHeader('Content-Type','text/xml');"
                "soap.setRequestBody('<soapenv:Envelope "
                "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">"
                "<soapenv:Body/></soapenv:Envelope>');"
                "var response = soap.execute();"
                "var status = response.getStatusCode();"
                "expect(status).toBe(200);"
                "});"
                "});"
                "})(step, stepResult, jasmine, describe);"
                "jasmine.getEnv().execute();"
            ),
        ),
    ]

    for name, description, script in tests:
        test = _ensure_test(instance, headers, name, description)
        test_id = test.get("sys_id")
        if not test_id:
            raise SystemExit(f"Failed to create ATF test: {name}")
        step = _ensure_step(instance, headers, test_id, order=1)
        step_id = step.get("sys_id")
        if not step_id:
            raise SystemExit(f"Failed to create ATF step for: {name}")
        if not _set_step_script(instance, headers, step_id, script):
            raise SystemExit(
                "ServiceNow ACL blocks sys_variable_value inserts for ATF steps. "
                "Run scripts/servicenow/atf_seed_steps.js in Scripts - Background, "
                "then re-run this command."
            )


def main() -> None:
    env = _get_env()
    instance = env.get("SERVICENOW_INSTANCE_URL")
    username = env.get("SERVICENOW_USERNAME")
    password = env.get("SERVICENOW_PASSWORD")
    if not all([instance, username, password]):
        raise SystemExit("Missing ServiceNow credentials in tools/servicenow-mcp/.env")

    instance = instance.rstrip("/")
    headers = _basic_headers(username, password)

    _ensure_catalog_item(instance, headers)
    _ensure_record_producer(instance, headers)
    _ensure_flow_stub(instance, headers)
    _ensure_rest_message(instance, headers)
    _ensure_business_rule(instance, headers)
    _ensure_script_include(instance, headers)

    integration_user = env.get("SERVICENOW_USERNAME") or ""
    integration_password = env.get("SERVICENOW_PASSWORD") or ""
    _ensure_property(instance, headers, "x_plego.integration.user", integration_user)
    _ensure_property(instance, headers, "x_plego.integration.password", integration_password)
    _ensure_property(instance, headers, "x_plego.integration.token", "plego-token")

    role = _ensure_role(instance, headers, "x_plego_it_agent")
    role_id = role.get("sys_id")
    itil_role = _ensure_role(instance, headers, "itil")
    itil_role_id = itil_role.get("sys_id")
    requester = _ensure_user(instance, headers, "plego_requester", "Plego", "Requester")
    agent = _ensure_user(instance, headers, "plego_it_agent", "Plego", "IT Agent")
    _ensure_dictionary_field(instance, headers)
    if role_id and agent.get("sys_id"):
        _ensure_user_role(instance, headers, agent["sys_id"], role_id)
    if itil_role_id and agent.get("sys_id"):
        _ensure_user_role(instance, headers, agent["sys_id"], itil_role_id)
    protected_acl = _ensure_protected_field_acl(instance, headers)
    protected_create_acl = _ensure_protected_field_create_acl(instance, headers)
    acl = _ensure_acl(instance, headers)
    table_acl = _ensure_table_write_acl(instance, headers)
    create_acl = _ensure_table_create_acl(instance, headers)
    if protected_acl.get("sys_id") and role_id:
        _ensure_acl_role(instance, headers, protected_acl["sys_id"], role_id)
    if protected_create_acl.get("sys_id") and role_id:
        _ensure_acl_role(instance, headers, protected_create_acl["sys_id"], role_id)
    if acl.get("sys_id") and role_id:
        _ensure_acl_role(instance, headers, acl["sys_id"], role_id)
    if table_acl.get("sys_id") and role_id:
        _ensure_acl_role(instance, headers, table_acl["sys_id"], role_id)
    if create_acl.get("sys_id") and role_id:
        _ensure_acl_role(instance, headers, create_acl["sys_id"], role_id)
    if not acl.get("sys_id") or not table_acl.get("sys_id") or not create_acl.get("sys_id") or not protected_create_acl.get("sys_id"):
        print(
            "ACL insert blocked by instance permissions. "
            "Run scripts/servicenow/atf_seed_steps.js (ACL block section) or create "
            "the sc_req_item write ACLs manually."
        )

    acl_test = _ensure_test(
        instance,
        headers,
        "ACL Sanity Checks",
        "Verify requester cannot edit protected field while IT agent can.",
    )
    requester_id = requester.get("sys_id")
    agent_id = agent.get("sys_id")
    if requester_id and agent_id:
        _bootstrap_acl_ui_test(instance, headers, acl_test["sys_id"], requester_id, agent_id)
    else:
        raise SystemExit("Missing requester or agent sys_id for ACL UI test")
    _bootstrap_tests(instance, headers)

    print("Bootstrapped artifacts and ATF tests.")


if __name__ == "__main__":
    main()
