define(function(require) {
  // load third-party javascript libraries
  var $ = require('jquery'),
      _ = require('underscore'),
      Backbone = require('backbone');

  // user-defined modules
  var TranscriptTableTemplate = require('text!jstemplates/transcript_table.html');
  var TranscriptCollection = require('collections/transcripts');

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
      return self;
    }

  });

  return TranscriptTableView;
});