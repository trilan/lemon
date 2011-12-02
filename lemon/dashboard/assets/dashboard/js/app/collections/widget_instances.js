dashboard.collections.WidgetInstances = Backbone.Collection.extend({

  model: dashboard.models.WidgetInstance,
  url:   function() { return __dashboard_widget_instances_url__; },

  initialize: function() {
    this.bind("add", this.addWidgetInstance, this);
  },

  addWidgetInstance: function() {
    this.fetch();
  }

});

dashboard.collections.widgetInstances = new dashboard.collections.WidgetInstances;
