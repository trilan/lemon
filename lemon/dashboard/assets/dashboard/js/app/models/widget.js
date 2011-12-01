dashboard.models.Widget = Backbone.Model.extend({

  viewClass: function() {
    return dashboard.views[this.get("viewName")];
  }

});
