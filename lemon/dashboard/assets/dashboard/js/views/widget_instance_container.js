dashboard.views.WidgetInstanceContainer = dashboard.views.Template.extend({

  tagName: "li",
  className: "dashboard-widget-instance-container",
  templateId: "dashboard/js/templates/widget_instance_container",

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

    this.$(".dashboard-widget-instance-body").append(this.model.view().el);
    return this;
  },

  templateContext: function() {
    var data = this.model.toJSON();
    data["widget"] = this.model.widget().toJSON();
    return data
  },

  destroyModel: function() {
    this.model.destroy();
  }

});
