var PlegoAjax = Class.create();
PlegoAjax.prototype = Object.extendsObject(AbstractAjaxProcessor, {
  /**
   * TODO: Return a default assignment group for the client.
   * Use in client scripts to auto-populate fields.
   */
  getDefaultGroup: function () {
    return '';
  },

  type: 'PlegoAjax'
});
