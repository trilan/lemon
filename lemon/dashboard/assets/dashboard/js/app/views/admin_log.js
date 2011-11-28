dashboard.views.AdminLog = dashboard.views.Template.extend({

  tagName: "div",
  className: "dashboard-admin-log-instance",
  templateId: "dashboard-admin-log-template",

  initialize: function() {
    dashboard.views.Template.prototype.initialize.call(this);
    if (dashboard.collections.adminLogEntries.length !== 0) {
      this.render();
    }
    dashboard.collections.adminLogEntries.bind("refresh", this.render);
  },

  render: function() {
    dashboard.views.Template.prototype.render.call(this);
    this.$("tr:last").addClass("last");
    return this;
  },

  templateContext: function() {
    return {entries: dashboard.collections.adminLogEntries.toJSON()};
  }

});
