dashboard.collections.AdminApps = Backbone.Collection.extend({

  model: dashboard.models.AdminApp

});

dashboard.collections.adminApps = new dashboard.collections.AdminApps;
