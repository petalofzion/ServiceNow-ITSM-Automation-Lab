import os
import sys
import requests
import json
from pathlib import Path

def load_env():
    env_path = Path("tools/servicenow-mcp/.env")
    config = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    config[k] = v
    return config

def main():
    config = load_env()
    instance_url = config.get("SERVICENOW_INSTANCE_URL")
    username = config.get("SERVICENOW_USERNAME")
    password = config.get("SERVICENOW_PASSWORD")

    if not instance_url or not username:
        print("Error: Missing credentials in .env")
        sys.exit(1)

    print(f"Connecting to {instance_url} as {username}...")

    target_number = "TES0001029"
    
    # 1. Try to find it as a SUITE result first
    print(f"Checking sys_atf_test_suite_result for {target_number}...")
    url = f"{instance_url}/api/now/table/sys_atf_test_suite_result"
    params = {
        "sysparm_query": f"number={target_number}",
        "sysparm_limit": 1,
        "sysparm_fields": "sys_id,status,number,sys_created_on"
    }
    
    resp = requests.get(url, auth=(username, password), params=params)
    suite_id = None
    
    if resp.status_code == 200:
        results = resp.json().get("result", [])
        if results:
            suite = results[0]
            print(f"Found Suite Result: {suite['number']}")
            print(f"Suite Status: {suite['status']}")
            print(f"Created: {suite['sys_created_on']}")
            suite_id = suite['sys_id']
        else:
            print("Not found in sys_atf_test_suite_result.")

    # 2. If not a suite, check if it's a test result (fallback)
    if not suite_id:
        print(f"Checking sys_atf_test_result for {target_number}...")
        url_test = f"{instance_url}/api/now/table/sys_atf_test_result"
        resp_test = requests.get(url_test, auth=(username, password), params=params)
        if resp_test.status_code == 200:
            results = resp_test.json().get("result", [])
            if results:
                test_res = results[0]
                print(f"Found Test Result: {test_res['number']}")
                # If it's a test result, get its parent suite to see context
                # But user insists it is a suite result. 
                # Let's see what happens.
    
    # 3. If we found a suite, fetch its children
    if suite_id:
        print("\nFetching child test results...")
        child_url = f"{instance_url}/api/now/table/sys_atf_test_result"
        # 'parent' is the field referencing the suite result
        child_params = {
            "sysparm_query": f"parent={suite_id}",
            "sysparm_fields": "sys_id,test_name,status,output,number,run_time"
        }
        resp_child = requests.get(child_url, auth=(username, password), params=child_params)
        children = resp_child.json().get("result", [])
        
        print(f"Found {len(children)} tests in this suite.")
        for child in children:
            status = child.get('status', 'unknown')
            icon = "✅" if status == "success" else "❌"
            name = child.get('test_name', 'Unknown')
            num = child.get('number', 'NO_NUM')
            duration = child.get('run_time', '')
            print(f"{icon} {num}: {name} - {status} ({duration})")
            if status != "success":
                 print(f"    Output: {child.get('output', '').strip()}")

if __name__ == "__main__":
    main()