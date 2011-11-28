dashboard.models.WidgetInstance = Backbone.Model.extend({

  defaults: {
    column: "left",
    position: 1
  },

  widget: function() {
    return dashboard.collections.widgets.get(this.get("widget"));
  },

  view: function() {
    var viewClass = this.widget().viewClass();
    return new viewClass({model: this});
  }

});
