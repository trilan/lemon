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
