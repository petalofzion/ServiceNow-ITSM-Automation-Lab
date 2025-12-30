var PlegoApprovalPolicy = Class.create();
PlegoApprovalPolicy.prototype = {
  initialize: function () {},

  /**
   * TODO: Enforce ITIL-ish approval requirements.
   * Example: high priority requests require manager + IT approval.
   * @param {GlideRecord} requestGr
   * @returns {Boolean}
   */
  requiresDualApproval: function (requestGr) {
    return requestGr.getValue('priority') === '1';
  },

  type: 'PlegoApprovalPolicy'
};
