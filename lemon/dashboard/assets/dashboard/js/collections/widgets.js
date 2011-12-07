dashboard.collections.Widgets = Backbone.Collection.extend({

  model: dashboard.models.Widget,
  url:   function() { return __dashboard_widget_instances_url__; }

});

dashboard.collections.widgets = new dashboard.collections.Widgets;
