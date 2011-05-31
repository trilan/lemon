dashboard.views.Index = dashboard.views.Template.extend({

  tagName:    "div",
  className:  "dashboard-index",
  templateId: "dashboard-index-template",

  initialize: function() {
    _.bindAll(this, "updateConnection");
    dashboard.views.Template.prototype.initialize.call(this);

    this.leftColumn = new dashboard.views.Column({column: "left"});
    this.leftColumn.bind("render", this.updateConnection);

    this.rightColumn = new dashboard.views.Column({column: "right"});
    this.rightColumn.bind("render", this.updateConnection);

    this.render();
  },

  render: function() {
    dashboard.views.Template.prototype.render.call(this);

    this.$(".dashboard-left-column").append(this.leftColumn.el);
    this.$(".dashboard-right-column").append(this.rightColumn.el);

    return this;
  },

  updateConnection: function() {
    $(this.rightColumn.el).sortable("option", "connectWith", $(this.leftColumn.el));
    $(this.leftColumn.el).sortable("option", "connectWith", $(this.rightColumn.el));
  }

});
