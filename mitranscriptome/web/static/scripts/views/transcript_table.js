define([
  'jquery', 
  'underscore', 
  'backbone',
  'text!jstemplates/transcript_table.html',
  'collections/transcripts',
  'tablesorter',
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
      self.listenTo(self.collection, 'remove', self.render);
    },
    
    render: function() {
      console.log('rendering');
      var self = this;
      // render the collection to html
      self.$el.html(self.template({ 'transcriptCollection': self.collection }));
      // add tablesorter functionality to table
      $('#transcripts_table').tablesorter();
      return self;
    }

  });

  return TranscriptTableView;
});