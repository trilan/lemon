//= require_self
//= require models
//= require collections
//= require views
//= require controllers
//= require templates

(function() {

  this.dashboard = {
    views: {},
    controllers: {},
    models: {},
    collections: {}
  };

  $(function() {
    new dashboard.controllers.Widgets({id: "dashboard"});
    Backbone.history.start();
  });

})();
