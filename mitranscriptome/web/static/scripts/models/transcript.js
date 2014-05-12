/**
 * 
 */
define([
  'underscore',
  'backbone'
], function(_, Backbone) {

  var Transcript = Backbone.Model.extend({
    idAttribute: 'transcript_id',
    initialize: function() {
      console.log("Transcript Model created");
  	}
  });
  
  return Transcript;
});