dashboard.views.WidgetInstanceContainer = dashboard.views.Template.extend({

  tagName: "li",
  className: "dashboard-widget-instance-container",
  templateId: "dashboard-widget-instance-container-template",

  events: {
    "click .dashboard-widget-instance-tools-close": "destroyModel",
  },

  initialize: function() {
    _.bindAll(this, "render", "destroyModel", "remove");
    this.model.bind("remove", this.remove);
  },

  render: function() {
    dashboard.views.Template.prototype.render.call(this);
    $(this.el).data("widgetInstance", this.model);

    this.$(".dashboard-widget-instance-body").append(this.model.view().render().el);
    return this;
  },

  destroyModel: function() {
    this.model.destroy();
  }

});
