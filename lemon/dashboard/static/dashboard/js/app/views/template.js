dashboard.views.Template = Backbone.View.extend({

  initialize: function() {
    _.bindAll(this, "render", "template");
  },

  render: function() {
    $(this.el).html(this.template(this.templateContext()));
    return this;
  },

  template: function(context) {
    return this.compileTemplate(this.templateId)(context);
  },

  compileTemplate: _.memoize(function(templateId) {
    return Handlebars.compile($("#" + templateId).html());
  }),

  templateContext: function() {
    return {}
  }

});
