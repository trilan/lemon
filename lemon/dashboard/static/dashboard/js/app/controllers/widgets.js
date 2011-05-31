dashboard.controllers.Widgets = Backbone.Controller.extend({

  routes: {
    "":     "index",
    "add":  "add",
  },

  initialize: function(options) {
    this.el = $("#" + options.id);

    this.indexView = new dashboard.views.Index;
    this.addView   = new dashboard.views.Add;
  },

  index: function() {
    this.switchTo(this.indexView);
  },

  add: function() {
    this.switchTo(this.addView);
  },

  switchTo: function(view) {
    $(this.el).empty().append(view.el)
  }

});
