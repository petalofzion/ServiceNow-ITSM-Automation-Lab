// Run in Scripts - Background once to seed ATF step scripts.
(function () {
  var SCRIPT_VAR = "989d9e235324220002c6435723dc3484";
  var STEP_CONFIG = "41de4a935332120028bc29cac2dc349a";

  function setStepScript(testName, script) {
    var test = new GlideRecord("sys_atf_test");
    test.addQuery("name", testName);
    test.query();
    if (!test.next()) {
      gs.print("Missing test: " + testName);
      return;
    }

    var step = new GlideRecord("sys_atf_step");
    step.addQuery("test", test.getUniqueValue());
    step.addQuery("step_config", STEP_CONFIG);
    step.orderBy("order");
    step.query();
    if (!step.next()) {
      gs.print("Missing step for test: " + testName);
      return;
    }

    var value = new GlideRecord("sys_variable_value");
    value.addQuery("document", "sys_atf_step");
    value.addQuery("document_key", step.getUniqueValue());
    value.addQuery("variable", SCRIPT_VAR);
    value.query();
    if (!value.next()) {
      value.initialize();
      value.document = "sys_atf_step";
      value.document_key = step.getUniqueValue();
      value.variable = SCRIPT_VAR;
    }
    value.value = script;
    if (value.isNewRecord()) {
      value.insert();
    } else {
      value.update();
    }
    gs.print("Seeded step script for: " + testName);
  }

  setStepScript(
    "Catalog Access Request Submission",
    [
      "(function(step, stepRunner, jasmine, describe) {",
      "describe('Catalog Access Request Submission', function() {",
      "it('creates request and ritm', function() {",
      "var item = new GlideRecord('sc_cat_item');",
      "item.addQuery('name','Access Request');",
      "item.query();",
      "expect(item.next()).toBe(true);",
      "var req = new GlideRecord('sc_request');",
      "req.initialize();",
      "req.requested_for = gs.getUserID();",
      "req.short_description = 'ATF Access Request';",
      "var reqId = req.insert();",
      "expect(gs.nil(reqId)).toBe(false);",
      "var ritm = new GlideRecord('sc_req_item');",
      "ritm.initialize();",
      "ritm.request = reqId;",
      "ritm.cat_item = item.getUniqueValue();",
      "ritm.short_description = 'ATF Access Request Item';",
      "var ritmId = ritm.insert();",
      "expect(gs.nil(ritmId)).toBe(false);",
      "});",
      "});",
      "})(step, stepResult, jasmine, describe);",
      "jasmine.getEnv().execute();",
    ].join("")
  );

  setStepScript(
    "Record Producer Creates Incident",
    [
      "(function(step, stepRunner, jasmine, describe) {",
      "describe('Record Producer Creates Incident', function() {",
      "it('creates incident via producer script', function() {",
      "var producer = new GlideRecord('sc_cat_item_producer');",
      "producer.addQuery('name','Report an Incident');",
      "producer.query();",
      "expect(producer.next()).toBe(true);",
      "var current = new GlideRecord(producer.table_name + '');",
      "current.initialize();",
      "eval(producer.script + '');",
      "expect(gs.nil(current.getUniqueValue())).toBe(false);",
      "var inc = new GlideRecord('incident');",
      "expect(inc.get(current.getUniqueValue())).toBe(true);",
      "});",
      "});",
      "})(step, stepResult, jasmine, describe);",
      "jasmine.getEnv().execute();",
    ].join("")
  );

  setStepScript(
    "Access Request Flow Trigger",
    [
      "(function(step, stepRunner, jasmine, describe) {",
      "describe('Access Request Flow Trigger', function() {",
      "it('flow exists and is active', function() {",
      "var flow = new GlideRecord('sys_hub_flow');",
      "flow.addQuery('name','Access Request Approval');",
      "flow.query();",
      "expect(flow.next()).toBe(true);",
      "expect(flow.active == true || flow.active == 'true').toBe(true);",
      "});",
      "});",
      "})(step, stepResult, jasmine, describe);",
      "jasmine.getEnv().execute();",
    ].join("")
  );

  setStepScript(
    "Access Request Approval Path",
    [
      "(function(step, stepRunner, jasmine, describe) {",
      "describe('Access Request Approval Path', function() {",
      "it('marks approval requested on new RITM', function() {",
      "var item = new GlideRecord('sc_cat_item');",
      "item.addQuery('name','Access Request');",
      "item.query();",
      "expect(item.next()).toBe(true);",
      "var req = new GlideRecord('sc_request');",
      "req.initialize();",
      "req.requested_for = gs.getUserID();",
      "req.short_description = 'ATF Approval Request';",
      "var reqId = req.insert();",
      "expect(gs.nil(reqId)).toBe(false);",
      "var ritm = new GlideRecord('sc_req_item');",
      "ritm.initialize();",
      "ritm.request = reqId;",
      "ritm.cat_item = item.getUniqueValue();",
      "ritm.short_description = 'ATF Approval RITM';",
      "var ritmId = ritm.insert();",
      "expect(gs.nil(ritmId)).toBe(false);",
      "var check = new GlideRecord('sc_req_item');",
      "expect(check.get(ritmId)).toBe(true);",
      "expect((check.approval + '') == 'requested').toBe(true);",
      "});",
      "});",
      "})(step, stepResult, jasmine, describe);",
      "jasmine.getEnv().execute();",
    ].join("")
  );

  setStepScript(
    "Smoke Logging and Script Includes",
    [
      "(function(step, stepRunner, jasmine, describe) {",
      "describe('Smoke Logging and Script Includes', function() {",
      "it('writes integration log entry', function() {",
      "var logger = new PlegoIntegrationLogger();",
      "var tag = 'ATF_LOG_' + gs.generateGUID();",
      "logger.log(tag);",
      "gs.sleep(1000);",
      "var log = new GlideRecord('syslog');",
      "log.addQuery('message','CONTAINS', tag);",
      "log.addQuery('sys_created_on','>=', gs.minutesAgoStart(5));",
      "log.query();",
      "expect(log.next()).toBe(true);",
      "});",
      "});",
      "})(step, stepResult, jasmine, describe);",
      "jasmine.getEnv().execute();",
    ].join("")
  );

  // ACL Sanity Checks now uses UI steps created via API bootstrap.

  setStepScript(
    "Outbound REST Success",
    [
      "(function(step, stepRunner, jasmine, describe) {",
      "describe('Outbound REST Success', function() {",
      "it('executes RESTMessageV2 successfully', function() {",
      "var user = gs.getProperty('x_plego.integration.user');",
      "var pass = gs.getProperty('x_plego.integration.password');",
      "expect(gs.nil(user)).toBe(false);",
      "expect(gs.nil(pass)).toBe(false);",
      "var endpoint = gs.getProperty('glide.servlet.uri') + ",
      "'api/now/table/sys_user?sysparm_limit=1';",
      "var msg = new sn_ws.RESTMessageV2();",
      "msg.setEndpoint(endpoint);",
      "msg.setHttpMethod('get');",
      "msg.setBasicAuth(user, pass);",
      "msg.setRequestHeader('Accept','application/json');",
      "var response = msg.execute();",
      "var status = response.getStatusCode();",
      "expect(status).toBe(200);",
      "var body = response.getBody();",
      "var parsed = JSON.parse(body);",
      "expect(parsed.result.length > 0).toBe(true);",
      "});",
      "});",
      "})(step, stepResult, jasmine, describe);",
      "jasmine.getEnv().execute();",
    ].join("")
  );

  setStepScript(
    "Outbound REST Failure Handling",
    [
      "(function(step, stepRunner, jasmine, describe) {",
      "describe('Outbound REST Failure Handling', function() {",
      "it('handles failure status codes', function() {",
      "var endpoint = gs.getProperty('glide.servlet.uri') + ",
      "'api/now/table/sys_user?sysparm_limit=1';",
      "var msg = new sn_ws.RESTMessageV2();",
      "msg.setEndpoint(endpoint);",
      "msg.setHttpMethod('get');",
      "msg.setBasicAuth('plego_bad_user','plego_bad_pass');",
      "var response = msg.execute();",
      "var status = response.getStatusCode();",
      "expect(status == 401 || status == 403).toBe(true);",
      "});",
      "});",
      "})(step, stepResult, jasmine, describe);",
      "jasmine.getEnv().execute();",
    ].join("")
  );

  setStepScript(
    "Inbound REST Creates Request",
    [
      "(function(step, stepRunner, jasmine, describe) {",
      "describe('Inbound REST Creates Request', function() {",
      "it('creates request via REST and rejects missing auth', function() {",
      "var user = gs.getProperty('x_plego.integration.user');",
      "var pass = gs.getProperty('x_plego.integration.password');",
      "expect(gs.nil(user)).toBe(false);",
      "expect(gs.nil(pass)).toBe(false);",
      "var base = gs.getProperty('glide.servlet.uri') + 'api/now/table/';",
      "var reqMsg = new sn_ws.RESTMessageV2();",
      "reqMsg.setEndpoint(base + 'sc_request');",
      "reqMsg.setHttpMethod('post');",
      "reqMsg.setBasicAuth(user, pass);",
      "reqMsg.setRequestHeader('Content-Type','application/json');",
      "reqMsg.setRequestBody(JSON.stringify({",
      "requested_for: gs.getUserID(),",
      "short_description: 'ATF Inbound Request'",
      "}));",
      "var reqResp = reqMsg.execute();",
      "var reqStatus = reqResp.getStatusCode();",
      "expect(reqStatus == 200 || reqStatus == 201).toBe(true);",
      "var reqBody = JSON.parse(reqResp.getBody());",
      "var reqId = reqBody.result.sys_id;",
      "expect(gs.nil(reqId)).toBe(false);",
      "var item = new GlideRecord('sc_cat_item');",
      "item.addQuery('name','Access Request');",
      "item.query();",
      "expect(item.next()).toBe(true);",
      "var ritmMsg = new sn_ws.RESTMessageV2();",
      "ritmMsg.setEndpoint(base + 'sc_req_item');",
      "ritmMsg.setHttpMethod('post');",
      "ritmMsg.setBasicAuth(user, pass);",
      "ritmMsg.setRequestHeader('Content-Type','application/json');",
      "ritmMsg.setRequestBody(JSON.stringify({",
      "request: reqId,",
      "cat_item: item.getUniqueValue(),",
      "short_description: 'ATF Inbound RITM'",
      "}));",
      "var ritmResp = ritmMsg.execute();",
      "var ritmStatus = ritmResp.getStatusCode();",
      "expect(ritmStatus == 200 || ritmStatus == 201).toBe(true);",
      "var badMsg = new sn_ws.RESTMessageV2();",
      "badMsg.setEndpoint(base + 'sc_request');",
      "badMsg.setHttpMethod('post');",
      "badMsg.setRequestHeader('Content-Type','application/json');",
      "badMsg.setRequestBody(JSON.stringify({",
      "requested_for: gs.getUserID(),",
      "short_description: 'ATF Inbound Request (no auth)'",
      "}));",
      "var badResp = badMsg.execute();",
      "var badStatus = badResp.getStatusCode();",
      "expect(badStatus == 401 || badStatus == 403).toBe(true);",
      "});",
      "});",
      "})(step, stepResult, jasmine, describe);",
      "jasmine.getEnv().execute();",
    ].join("")
  );

  setStepScript(
    "SOAP Call Logged",
    [
      "(function(step, stepRunner, jasmine, describe) {",
      "describe('SOAP Call Logged', function() {",
      "it('executes SOAPMessageV2', function() {",
      "var user = gs.getProperty('x_plego.integration.user');",
      "var pass = gs.getProperty('x_plego.integration.password');",
      "expect(gs.nil(user)).toBe(false);",
      "expect(gs.nil(pass)).toBe(false);",
      "var endpoint = gs.getProperty('glide.servlet.uri') + ",
      "'api/now/table/sys_user?sysparm_limit=1';",
      "var soap = new sn_ws.SOAPMessageV2();",
      "soap.setEndpoint(endpoint);",
      "soap.setHttpMethod('get');",
      "soap.setBasicAuth(user, pass);",
      "soap.setRequestHeader('Content-Type','text/xml');",
      "soap.setRequestBody('<soapenv:Envelope ",
      "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">",
      "<soapenv:Body/></soapenv:Envelope>');",
      "var response = soap.execute();",
      "var status = response.getStatusCode();",
      "expect(status).toBe(200);",
      "});",
      "});",
      "})(step, stepResult, jasmine, describe);",
      "jasmine.getEnv().execute();",
    ].join("")
  );

  function ensureAcl() {
    var dict = new GlideRecord("sys_dictionary");
    dict.addQuery("name", "sc_req_item");
    dict.addQuery("element", "u_plego_protected");
    dict.query();
    if (!dict.next()) {
      dict.initialize();
      dict.name = "sc_req_item";
      dict.element = "u_plego_protected";
      dict.column_label = "Plego Protected";
      dict.internal_type = "string";
      dict.max_length = 160;
      dict.active = true;
      dict.insert();
    }

    var fieldAclId = "";
    var tableAclId = "";

    var fieldAcl = new GlideRecord("sys_security_acl");
    fieldAcl.addQuery("name", "sc_req_item.short_description");
    fieldAcl.addQuery("operation", "write");
    fieldAcl.addQuery("type", "field");
    fieldAcl.query();
    if (fieldAcl.next()) {
      fieldAclId = fieldAcl.getUniqueValue();
    } else {
      fieldAcl.initialize();
      fieldAcl.name = "sc_req_item.short_description";
      fieldAcl.operation = "write";
      fieldAcl.type = "field";
      fieldAcl.active = true;
      fieldAcl.admin_overrides = true;
      fieldAcl.description = "Plego ACL for ATF sanity checks (manual seed)";
      fieldAclId = fieldAcl.insert();
    }

    var tableAcl = new GlideRecord("sys_security_acl");
    tableAcl.addQuery("name", "sc_req_item");
    tableAcl.addQuery("operation", "write");
    tableAcl.addQuery("type", "record");
    tableAcl.query();
    if (tableAcl.next()) {
      tableAclId = tableAcl.getUniqueValue();
    } else {
      tableAcl.initialize();
      tableAcl.name = "sc_req_item";
      tableAcl.operation = "write";
      tableAcl.type = "record";
      tableAcl.active = true;
      tableAcl.admin_overrides = true;
      tableAcl.description = "Plego record write ACL for ATF sanity checks (manual seed)";
      tableAclId = tableAcl.insert();
    }

    if (tableAclId) {
      var tableAclRecord = new GlideRecord("sys_security_acl");
      if (tableAclRecord.get(tableAclId)) {
        tableAclRecord.condition =
          "current.requested_for == gs.getUserID() || gs.hasRole('x_plego_it_agent')";
        tableAclRecord.script = "";
        tableAclRecord.update();
      }
    }

    var protectedAclId = "";
    var protectedAcl = new GlideRecord("sys_security_acl");
    protectedAcl.addQuery("name", "sc_req_item.u_plego_protected");
    protectedAcl.addQuery("operation", "write");
    protectedAcl.addQuery("type", "field");
    protectedAcl.query();
    if (protectedAcl.next()) {
      protectedAclId = protectedAcl.getUniqueValue();
    } else {
      protectedAcl.initialize();
      protectedAcl.name = "sc_req_item.u_plego_protected";
      protectedAcl.operation = "write";
      protectedAcl.type = "field";
      protectedAcl.active = true;
      protectedAcl.admin_overrides = true;
      protectedAcl.description = "Plego protected field ACL (manual seed)";
      protectedAclId = protectedAcl.insert();
    }

    if (!fieldAclId || !tableAclId) {
      gs.print("ACL insert failed.");
      return;
    }

    var role = new GlideRecord("sys_user_role");
    role.addQuery("name", "x_plego_it_agent");
    role.query();
    if (!role.next()) {
      role.initialize();
      role.name = "x_plego_it_agent";
      role.description = "Plego test role (manual seed)";
      role.insert();
      role.query();
      role.next();
    }

    var fieldLink = new GlideRecord("sys_security_acl_role");
    fieldLink.addQuery("sys_security_acl", fieldAclId);
    fieldLink.addQuery("sys_user_role", role.getUniqueValue());
    fieldLink.query();
    if (!fieldLink.next()) {
      fieldLink.initialize();
      fieldLink.sys_security_acl = fieldAclId;
      fieldLink.sys_user_role = role.getUniqueValue();
      fieldLink.insert();
    }

    var tableLink = new GlideRecord("sys_security_acl_role");
    tableLink.addQuery("sys_security_acl", tableAclId);
    tableLink.addQuery("sys_user_role", role.getUniqueValue());
    tableLink.query();
    if (!tableLink.next()) {
      tableLink.initialize();
      tableLink.sys_security_acl = tableAclId;
      tableLink.sys_user_role = role.getUniqueValue();
      tableLink.insert();
    }

    if (protectedAclId) {
      var protectedLink = new GlideRecord("sys_security_acl_role");
      protectedLink.addQuery("sys_security_acl", protectedAclId);
      protectedLink.addQuery("sys_user_role", role.getUniqueValue());
      protectedLink.query();
      if (!protectedLink.next()) {
        protectedLink.initialize();
        protectedLink.sys_security_acl = protectedAclId;
        protectedLink.sys_user_role = role.getUniqueValue();
        protectedLink.insert();
      }
    }

    gs.print("Seeded ACL + role link for sc_req_item write.");

    var itil = new GlideRecord("sys_user_role");
    itil.addQuery("name", "itil");
    itil.query();
    if (!itil.next()) {
      itil.initialize();
      itil.name = "itil";
      itil.description = "ITIL base role (manual seed)";
      itil.insert();
      itil.query();
      itil.next();
    }

    var agent = new GlideRecord("sys_user");
    agent.addQuery("user_name", "plego_it_agent");
    agent.query();
    if (agent.next()) {
      var agentRole = new GlideRecord("sys_user_has_role");
      agentRole.addQuery("user", agent.getUniqueValue());
      agentRole.addQuery("role", role.getUniqueValue());
      agentRole.query();
      if (!agentRole.next()) {
        agentRole.initialize();
        agentRole.user = agent.getUniqueValue();
        agentRole.role = role.getUniqueValue();
        agentRole.insert();
      }

      var itilRole = new GlideRecord("sys_user_has_role");
      itilRole.addQuery("user", agent.getUniqueValue());
      itilRole.addQuery("role", itil.getUniqueValue());
      itilRole.query();
      if (!itilRole.next()) {
        itilRole.initialize();
        itilRole.user = agent.getUniqueValue();
        itilRole.role = itil.getUniqueValue();
        itilRole.insert();
      }
    }
  }

  function getVarId(stepConfig, element) {
    var dict = new GlideRecord("var_dictionary");
    dict.addQuery("name", "STARTSWITH", "var__m_atf_input_variable_" + stepConfig);
    dict.addQuery("element", element);
    dict.query();
    if (dict.next()) {
      return dict.getUniqueValue();
    }
    gs.print("Missing var_dictionary for step " + stepConfig + " element " + element);
    return "";
  }

  function createUiStep(testId, stepConfig, order, description, inputs) {
    var step = new GlideRecord("sys_atf_step");
    step.initialize();
    step.test = testId;
    step.step_config = stepConfig;
    step.order = order;
    step.description = description;
    var stepId = step.insert();
    if (!stepId) {
      gs.print("Failed to create UI step: " + description);
      return;
    }

    var existing = new GlideRecord("sys_variable_value");
    existing.addQuery("document", "sys_atf_step");
    existing.addQuery("document_key", stepId);
    existing.query();
    while (existing.next()) {
      existing.deleteRecord();
    }

    for (var key in inputs) {
      if (!inputs.hasOwnProperty(key)) {
        continue;
      }
      var varId = getVarId(stepConfig, key);
      if (!varId) {
        continue;
      }
      var value = new GlideRecord("sys_variable_value");
      value.initialize();
      value.document = "sys_atf_step";
      value.document_key = stepId;
      value.variable = varId;
      value.value = inputs[key];
      value.insert();
    }
  }

  function ensureFieldOnForm(tableName, fieldName) {
    var sections = new GlideRecord("sys_ui_section");
    sections.addQuery("name", tableName);
    sections.orderBy("position");
    sections.query();
    if (!sections.hasNext()) {
      gs.print("Missing form section for table: " + tableName);
      return;
    }

    while (sections.next()) {
      var element = new GlideRecord("sys_ui_element");
      element.addQuery("sys_ui_section", sections.getUniqueValue());
      element.addQuery("element", fieldName);
      element.query();
      if (element.next()) {
        continue;
      }

      element.initialize();
      element.sys_ui_section = sections.getUniqueValue();
      element.element = fieldName;
      element.position = 100;
      element.insert();
    }
  }

  function seedAclUiSteps() {
    var test = new GlideRecord("sys_atf_test");
    test.addQuery("name", "ACL Sanity Checks");
    test.query();
    if (!test.next()) {
      gs.print("Missing test: ACL Sanity Checks");
      return;
    }

    var requester = new GlideRecord("sys_user");
    requester.addQuery("user_name", "plego_requester");
    requester.query();
    if (!requester.next()) {
      gs.print("Missing user: plego_requester");
      return;
    }

    var agent = new GlideRecord("sys_user");
    agent.addQuery("user_name", "plego_it_agent");
    agent.query();
    if (!agent.next()) {
      gs.print("Missing user: plego_it_agent");
      return;
    }

    var steps = new GlideRecord("sys_atf_step");
    steps.addQuery("test", test.getUniqueValue());
    steps.query();
    while (steps.next()) {
      steps.deleteRecord();
    }

    var IMPERSONATE = "071ee5b253331200040729cac2dc348d";
    var OPEN_FORM = "05317cd10b10220050192f15d6673af8";
    var FIELD_STATE = "1dfece935332120028bc29cac2dc3478";

    ensureFieldOnForm("sc_req_item", "u_plego_protected");

    createUiStep(test.getUniqueValue(), IMPERSONATE, 1, "Impersonate requester", {
      user: requester.getUniqueValue(),
    });
    createUiStep(test.getUniqueValue(), OPEN_FORM, 2, "Open sc_req_item form", {
      table: "sc_req_item",
      view: "",
      form_ui: "standard_ui",
      record_path: "record",
    });
    createUiStep(test.getUniqueValue(), FIELD_STATE, 3, "Requester cannot edit protected field", {
      table: "sc_req_item",
      read_only: "u_plego_protected",
      form_ui: "standard_ui",
    });
    createUiStep(test.getUniqueValue(), IMPERSONATE, 4, "Impersonate IT agent", {
      user: agent.getUniqueValue(),
    });
    createUiStep(test.getUniqueValue(), OPEN_FORM, 5, "Open sc_req_item form as agent", {
      table: "sc_req_item",
      view: "",
      form_ui: "standard_ui",
      record_path: "record",
    });
    createUiStep(test.getUniqueValue(), FIELD_STATE, 6, "Agent can edit protected field", {
      table: "sc_req_item",
      not_read_only: "u_plego_protected",
      form_ui: "standard_ui",
    });

    gs.print("Seeded ACL Sanity Checks UI steps.");
  }

  ensureAcl();
  seedAclUiSteps();
})();
