dashboard.views.AdminApps = dashboard.views.Template.extend({

  tagName: "div",
  className: "dashboard-admin-apps-instance",
  templateId: "dashboard/js/app/templates/admin_apps",

  initialize: function() {
    dashboard.views.Template.prototype.initialize.call(this);
    if (dashboard.collections.adminApps.length != 0) {
      this.render();
    }
    dashboard.collections.adminApps.bind("refresh", this.render);
  },

  render: function() {
    dashboard.views.Template.prototype.render.call(this);
    this.$(".app:last").addClass("last");
    this.$(".model:last-child").addClass("last");
    return this;
  },

  templateContext: function() {
    return {apps: dashboard.collections.adminApps.toJSON()};
  }

});
