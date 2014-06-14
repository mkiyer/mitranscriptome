define([
  'jquery', 
  'underscore', 
  'backbone',
  'text!jstemplates/transcript_table.html',
  'collections/transcripts',
  'tablesorter',
  'jqueryspin'
], function($, _, Backbone,
  TranscriptTableTemplate,
  TranscriptCollection) {
  
  // define view
  var TranscriptTableView = Backbone.View.extend({

    initialize: function(options) {
      var self = this;
      // attributes
      self.template = _.template(TranscriptTableTemplate);
      // register events
      // bind view to collection
      self.listenTo(self.collection, 'sync', self.render);
    },

    load: function(func_type) {
      var self = this;
      // show loading spinner
      self.$el.spin();
      // clear collection
      self.collection.reset();
      // update ajax parameters
      _.extend(self.collection.ajaxParams,
        { data: JSON.stringify({ func_type: func_type }) }
      );
      // trigger asynchronous load of new data (will call render() when done)
      self.collection.fetch(self.collection.ajaxParams);
    },

    render: function() {
      var self = this;
      // turn off loading spinner
      self.$el.spin(false);
      // render the collection to html
      self.$el.html(self.template({ 'transcriptCollection': self.collection }));
      // add tablesorter functionality to table
      $('#transcripts_table').tablesorter();
      return self;
    }

  });

  return TranscriptTableView;
});