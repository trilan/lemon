dashboard.views.Add = dashboard.views.Template.extend({

  tagName: "div",
  className: "dashboard-add",
  templateId: "dashboard-add-template",

  initialize: function() {
    dashboard.views.Template.prototype.initialize.call(this);
    _.bindAll(this, "addOne", "addAll");

    this.widgets = dashboard.collections.widgets;
    this.widgets.bind("refresh", this.render);
  },

  render: function() {
    dashboard.views.Template.prototype.render.call(this);
    this.addAll();
    return this;
  },

  addOne: function(widget) {
    var view = new dashboard.views.Widget({model: widget});
    this.$("#dashboard-widget-list").append(view.render().el);
  },

  addAll: function() {
    this.widgets.each(this.addOne);
  }

});
