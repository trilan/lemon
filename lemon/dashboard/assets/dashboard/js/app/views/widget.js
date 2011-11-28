dashboard.views.Widget = dashboard.views.Template.extend({

  tagName:    "li",
  className:  "dashboard-widget",
  templateId: "dashboard-widget-template",

  events: {
    "click .dashboard-widget-add-link": "add"
  },

  initialize: function() {
    dashboard.views.Template.prototype.initialize.call(this);
    _.bindAll(this, "add"),

    this.model.bind("change", this.render);
  },

  templateContext: function() {
    return this.model.toJSON();
  },

  add: function() {
    dashboard.collections.widgetInstances.create({
      widget: this.model.id
    });
    return false;
  }

});
