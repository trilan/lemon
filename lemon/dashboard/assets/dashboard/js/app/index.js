//= require_self
//= require models
//= require collections
//= require views
//= require routers
//= require templates

(function() {

  this.dashboard = {
    views: {},
    routers: {},
    models: {},
    collections: {}
  };

  $(function() {
    new dashboard.routers.Widgets({id: "dashboard"});
    Backbone.history.start();
  });

})();
