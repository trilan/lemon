dashboard.routers.Widgets = Backbone.Router.extend({

  routes: {
    "":     "main",
    "add":  "add",
  },

  initialize: function(options) {
    this.el = $("#" + options.id);

    this.mainView = new dashboard.views.Main;
    this.addView   = new dashboard.views.Add;

    $([this.mainView.el, this.addView.el]).hide().appendTo(this.el);
  },

  main: function() {
    this.switchTo(this.mainView);
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
