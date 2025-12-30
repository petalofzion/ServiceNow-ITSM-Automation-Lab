# Requirements Coverage Matrix

This document maps every responsibility and requirement from Plego’s ServiceNow Developer posting to: (1) ServiceNow artifacts to create, (2) ATF tests to prove it, and (3) exported evidence artifacts to attach in GitHub Releases. Keep it short, factual, and current.

## Coverage Map

| Responsibility / requirement | ServiceNow artifacts to create | ATF test(s) to prove it | Evidence artifacts to export |
| --- | --- | --- | --- |
| Develop/configure/customize ServiceNow applications & modules | Scoped app **Plego ITSM Automation Lab**, app files, update sets | ATF Smoke: app installs, tables exist | Update set export, app package, install logs |
| Workflows, Business Rules, UI Policies, Client Scripts, Script Includes | Flow Designer flows, Business Rules, UI Policies, Client Scripts, Script Includes + GlideAjax | ATF: flow triggers, BR validations, UI policies toggle, client script validation, Script Include callable | Update set exports, flow export, ATF run report |
| Service Catalogs, Record Producers, automated Request Workflows | Catalog Items (Access Request, New Laptop), Record Producer (Report Incident), request workflows | ATF: catalog submission creates request/ritm; record producer creates incident | Catalog XML export, update set, ATF run report |
| Performance Analytics dashboards & reports | PA indicators, dashboards, widgets, reports | ATF: PA dashboard renders seeded data | PA/dashboard exports, report exports, screenshots |
| Integrations via REST/SOAP, MID Server, external tools | Outbound REST messages, inbound Scripted REST API, SOAP stubs, MID Server notes | ATF: outbound call logged; inbound API creates record | REST/SOAP definitions, integration logs, MID Server evidence |
| Troubleshoot/resolve performance issues and stability | Performance logging, inefficient query + optimized version, indexed fields | ATF: performance baseline vs optimized check | Performance report, query logs, before/after metrics |
| Partner with analysts/stakeholders to understand requirements | Requirements contract in `docs/spec-architecture-requirements.md` and evidence map | ATF: traceability checks for key stories | Requirements doc snapshot, evidence map |
| Security, compliance, ITIL alignment | Roles, ACLs, audit history, ITIL-aligned categories/SLAs | ATF: restricted access by role, SLA attached | ACL export, audit logs, SLA export |
| Proficiency: JavaScript, Glide API, HTML/CSS, AngularJS | Script Includes, Client Scripts, UI scripts/templates; Service Portal widgets | ATF: UI script behavior, portal widget renders | Script exports, portal widget export, screenshots |
| Experience with ITSM/ITOM/HRSD/SecOps modules | ITSM-focused artifacts; stubs for ITOM/HRSD/SecOps in desired state | ATF: ITSM suite passes; module stubs validate | Module stub exports, ATF suite results |
| Strong Flow Designer, Workflow Editor, Service Portal customization | Flow Designer flows, legacy workflow stubs, Service Portal widgets | ATF: flow and portal widget validation | Flow export, workflow stub export, portal widget export |
| Hands-on REST/SOAP integrations | Scripted REST APIs, REST Message, SOAP Message | ATF: REST/SOAP invocation results | REST/SOAP exports, logs |

## Definition of Done

- [ ] Every responsibility above has at least one concrete ServiceNow artifact in the desired state.
- [ ] Every responsibility above has at least one ATF test in a named suite, or a documented manual check if ATF is not applicable.
- [ ] Every responsibility above has an exported evidence artifact attached to the release.
- [ ] `docs/success-metrics.md` updated with links to evidence and ATF run IDs.
- [ ] `ops/desired-state/` reflects the current scoped app configuration.
- [ ] `make demo` produces a complete `/artifacts` bundle.
