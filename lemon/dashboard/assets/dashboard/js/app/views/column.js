dashboard.views.Column = Backbone.View.extend({

  tagName: "ul",
  className: "dashboard-widget-instance-list",

  initialize: function() {
    _.bindAll(this, "render", "addOne", "addAll", "isThisColumn");

    this.column = this.options.column;
    dashboard.collections.widgetInstances.bind("refresh", this.render);
  },

  render: function() {
    $(this.el).data("columnView", this).empty();
    this.addAll();
    $(this.el).sortable({
      handle: ".dashboard-widget-instance-title",
      placeholder: "dashboard-widget-instance-placeholder",
      forcePlaceholderSize: true,
      update: this.updatePosition
    });
    this.trigger("render", this);
    return this;
  },

  addOne: function(widgetInstance) {
    var view = new dashboard.views.WidgetInstanceContainer({model: widgetInstance});
    $(this.el).append(view.render().el);
  },

  addAll: function() {
    var widgetInstances;
    widgetInstances = dashboard.collections.widgetInstances;
    widgetInstances = widgetInstances.select(this.isThisColumn);
    widgetInstances = _.sortBy(widgetInstances, this.getWidgetInstancePosition);
    _.each(widgetInstances, this.addOne);
  },

  isThisColumn: function(widgetInstance) {
    return widgetInstance.get("column") == this.column;
  },

  getWidgetInstancePosition: function(widgetInstance) {
    return widgetInstance.get("position");
  },

  updatePosition: function(event, ui) {
    if (!ui.item.parent().is(this)) return;
    ui.item.data("widgetInstance").set({
      column: $(this).data("columnView").column,
      position: ui.item.prevAll().length
    }).save();
  }

});
