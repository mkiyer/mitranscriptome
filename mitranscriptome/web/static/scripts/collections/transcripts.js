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

    load: function(functype, lineage) {
      var self = this;
      // clear collection
      self.reset();
      // load
      var ajaxParams = _.extend(self.ajaxParams,
        { data: JSON.stringify({ functype: functype, lineage: lineage }) }
      );
      this.fetch(self.ajaxParams);
    }

  });

  return TranscriptCollection;
});