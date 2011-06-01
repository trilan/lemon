dashboard.views.TextWidget = Backbone.View.extend({

  tagName: "div",
  className: "dashboard-text-widget-instance",

  render: function() {
    $(this.el).html(this.model.widget().get("text"));
    return this;
  }

});
