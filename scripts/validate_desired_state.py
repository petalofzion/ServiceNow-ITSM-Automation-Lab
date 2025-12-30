from __future__ import annotations

from pathlib import Path
from typing import List, Optional, cast

import yaml
from pydantic import BaseModel, Field, RootModel


class Role(BaseModel):
    name: str
    description: str


class Acl(BaseModel):
    table: str
    operation: str
    roles: List[str]


class RolesAclsModel(BaseModel):
    roles: List[Role]
    acls: List[Acl]


class Variable(BaseModel):
    name: str
    type: str
    table: Optional[str] = None
    choices: Optional[List[str]] = None


class CatalogItem(BaseModel):
    name: str
    description: Optional[str] = None
    variables: List[Variable]
    flow_trigger: Optional[str] = None


class RecordProducer(BaseModel):
    name: str
    table: str
    variables: List[Variable]


class FlowTrigger(BaseModel):
    type: str
    catalog_item: Optional[str] = None
    condition: Optional[str] = None


class FlowStep(BaseModel):
    action: str
    role: Optional[str] = None
    assignment_group: Optional[str] = None


class Flow(BaseModel):
    name: str
    trigger: FlowTrigger
    steps: List[FlowStep]


class CatalogModel(BaseModel):
    items: List[CatalogItem] = Field(default_factory=list)
    record_producers: List[RecordProducer] = Field(default_factory=list)
    flows: List[Flow] = Field(default_factory=list)


class BusinessRule(BaseModel):
    name: str
    table: str
    when: str
    operation: str
    description: Optional[str] = None


class UiPolicyAction(BaseModel):
    field: str
    visible: Optional[bool] = None
    mandatory: Optional[bool] = None


class UiPolicy(BaseModel):
    name: str
    table: str
    condition: str
    actions: List[UiPolicyAction]


class ClientScript(BaseModel):
    name: str
    table: str
    type: str
    description: Optional[str] = None


class ScriptInclude(BaseModel):
    name: str
    scope: str
    api: str
    description: Optional[str] = None


class ScriptsModel(BaseModel):
    business_rules: List[BusinessRule] = Field(default_factory=list)
    ui_policies: List[UiPolicy] = Field(default_factory=list)
    client_scripts: List[ClientScript] = Field(default_factory=list)
    script_includes: List[ScriptInclude] = Field(default_factory=list)


class OutboundRest(BaseModel):
    name: str
    endpoint: str
    method: str
    trigger: str
    payload_template: Optional[str] = None


class InboundRest(BaseModel):
    name: str
    endpoint: str
    method: str
    table: str


class SoapIntegration(BaseModel):
    name: str
    endpoint: str
    method: str
    action: str


class IntegrationsModel(BaseModel):
    outbound_rest: List[OutboundRest] = Field(default_factory=list)
    inbound_rest: List[InboundRest] = Field(default_factory=list)
    soap: List[SoapIntegration] = Field(default_factory=list)


class DashboardWidget(BaseModel):
    name: str
    type: str
    source: str
    table: str


class Dashboard(BaseModel):
    name: str
    description: Optional[str] = None
    widgets: List[DashboardWidget]


class DashboardsModel(RootModel[List[Dashboard]]):
    pass


class TestCase(BaseModel):
    name: str
    type: str
    covers: List[str]


class TestSuite(BaseModel):
    name: str
    tests: List[TestCase]


class TestsModel(BaseModel):
    suites: List[TestSuite]


DESIRED_STATE_SCHEMAS = {
    "roles_acls.yml": ("roles_acls", RolesAclsModel),
    "catalog.yml": ("catalog", CatalogModel),
    "scripts.yml": ("scripts", ScriptsModel),
    "integrations.yml": ("integrations", IntegrationsModel),
    "dashboards.yml": ("dashboards", DashboardsModel),
    "tests.yml": ("tests", TestsModel),
}


def _validate_model(model_cls: type[BaseModel], data: dict) -> None:
    if hasattr(model_cls, "model_validate"):
        model_cls.model_validate(data)
    else:
        model_cls.parse_obj(data)


def validate_desired_state(directory: Path) -> None:
    for filename, (root_key, model_cls) in DESIRED_STATE_SCHEMAS.items():
        path = directory / filename
        payload = yaml.safe_load(path.read_text())
        if root_key not in payload:
            raise ValueError(f"{filename} missing root key '{root_key}'")
        _validate_model(cast(type[BaseModel], model_cls), payload[root_key])


if __name__ == "__main__":
    desired_state_dir = Path("ops/desired-state")
    validate_desired_state(desired_state_dir)
    print("Desired-state schemas validated successfully.")
