dashboard.controllers.Widgets = Backbone.Controller.extend({

  routes: {
    "":     "index",
    "add":  "add",
  },

  initialize: function(options) {
    this.el = $("#" + options.id);

    this.indexView = new dashboard.views.Index;
    this.addView   = new dashboard.views.Add;

    $([this.indexView.el, this.addView.el]).hide().appendTo(this.el);
  },

  index: function() {
    this.switchTo(this.indexView);
  },

  add: function() {
    this.switchTo(this.addView);
  },

  switchTo: function(view) {
    if (this.activeView) {
      $(this.activeView.el).hide();
    }
    $(view.el).show();
    this.activeView = view;
  }

});
