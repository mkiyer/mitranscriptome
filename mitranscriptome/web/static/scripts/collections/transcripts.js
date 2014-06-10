/**
 * 
 */
define([
  'underscore',
  'backbone',
  'models/transcript'
], function(_, Backbone, Transcript) {

  var TranscriptCollection = Backbone.Collection.extend({
    model: Transcript,
    url: '/transcripts',
    ajaxParams: { 
      type: 'post', 
      contentType: 'application/json', 
      dataType: 'json' 
    },

    parse: function(response) {
        // console.log(JSON.stringify(response.results));
        return response.results;
    },

    load: function(func_type) {
      var self = this;
      // clear collection
      self.reset();
      // load
      var ajaxParams = _.extend(self.ajaxParams,
        { data: JSON.stringify({func_type: func_type }) }
      );
      this.fetch(self.ajaxParams);
    }

  });

  return TranscriptCollection;
});