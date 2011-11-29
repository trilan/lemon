dashboard.views.Template = Backbone.View.extend({

  initialize: function() {
    _.bindAll(this, "render", "template");
  },

  render: function() {
    $(this.el).html(this.template(this.templateContext()));
    return this;
  },

  template: function(context) {
    return Handlebars.templates[this.templateId](context);
  },

  templateContext: function() {
    return {}
  }

});
