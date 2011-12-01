dashboard.collections.AdminLogEntries = Backbone.Collection.extend({

  model: dashboard.models.AdminLogEntry,
  url: function() {
    return __admin_log_entries_url__;
  }

});

dashboard.collections.adminLogEntries = new dashboard.collections.AdminLogEntries;
