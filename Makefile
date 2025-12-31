.PHONY: build test export demo mcp-start check ci

MCP_SERVER_DIR ?= tools/servicenow-mcp

build:
	@echo "Applying desired state and seeding data..."
	python3 scripts/sn_apply_desired_state.py
	python3 scripts/sn_seed_data.py

test:
	@echo "Running ATF suites..."
	python3 scripts/sn_bootstrap_atf_tests.py
	python3 scripts/sn_ensure_atf_suites.py
	python3 scripts/sn_run_atf.py --suite "$(SUITE)"

SUITE ?= Smoke

export:
	@echo "Exporting artifacts and capturing evidence..."
	python3 scripts/sn_export_artifacts.py
	python3 scripts/sn_capture_evidence.py

demo: build test export
	@echo "Demo complete. Artifacts available in ./artifacts"

mcp-start:
	@echo "Starting ServiceNow MCP server from $(MCP_SERVER_DIR)..."
	@echo "Update tools/servicenow-mcp/README.md with exact start command."

check:
	@echo "Running lint, type checks, tests, and schema validation..."
	python3 -m ruff check .
	python3 -m black --check .
	python3 -m mypy .
	python3 -m pytest
	python3 scripts/validate_desired_state.py

ci: check
