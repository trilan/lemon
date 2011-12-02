dashboard.views.Add = dashboard.views.Template.extend({

  tagName: "div",
  className: "dashboard-add",
  templateId: "dashboard/js/app/templates/add",

  initialize: function() {
    var render;

    dashboard.views.Template.prototype.initialize.call(this);
    _.bindAll(this, "addOne", "addAll");

    dashboard.collections.widgetInstances.bind("reset", this.render);
    dashboard.collections.widgetInstances.bind("remove", this.render);
  },

  render: function() {
    dashboard.views.Template.prototype.render.call(this);
    this.addAll();
    return this;
  },

  templateContext: function() {
    return {
      title: __dashboard_add_view_title__,
      button: __dashboard_index_view_title__
    };
  },

  addOne: function(widget) {
    var view = new dashboard.views.Widget({model: widget});
    this.$("#dashboard-widget-list").append(view.render().el);
  },

  addAll: function() {
    var usedWidgetIds, availableWidgets;
    usedWidgetIds = dashboard.collections.widgetInstances.pluck("widget");
    availableWidgets = dashboard.collections.widgets.select(function(widget) {
      return _.indexOf(usedWidgetIds, widget.id) === -1;
    });
    _(availableWidgets).each(this.addOne);
  }

});
