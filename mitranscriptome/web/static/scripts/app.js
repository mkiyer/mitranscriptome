define([
  'jquery',
  'underscore',
  'backbone',
  'd3',
  'collections/transcripts',
  'views/transcript_table'
], function($, _, Backbone, d3,
    TranscriptCollection,
    TranscriptTableView) {

  // collections
  var selectedTranscripts = new TranscriptCollection;

  // views
  var transcriptTableView = new TranscriptTableView({ 
    el: '#div-transcript-table',
    collection: selectedTranscripts
  });
  
  // load transcripts
  selectedTranscripts.load('CLAT', 'breast');
 
  // button click functions
  function toggle_visibility(id) {
    var e = document.getElementById(id);
    if(e.style.display == 'block')
      e.style.display = 'none';
    else
      e.style.display = 'block';
  }
  function toggle_off(id) {
    var e = document.getElementById(id);
    e.style.display = 'none';
  }
  function toggle_on(id) {
    var e = document.getElementById(id);
    e.style.display = 'block';
  }
  // button events
  $('#Choose_Study_Btn').click(function() {
	toggle_off('Home');
	toggle_off('Methods');
	toggle_off('Downloads');
	toggle_on('Choose_Study');
	toggle_off('LATs');
	toggle_off('CATs');
	toggle_off('CLATs');
  });
  $('#Methods_Btn').click(function() {
	toggle_off('Home');
	toggle_on('Methods');
	toggle_off('Downloads');
	toggle_off('Choose_Study');
	toggle_off('LATs');
	toggle_off('CATs');
	toggle_off('CLATs');
  });
  $('#Downloads_Btn').click(function() {
	toggle_off('Home');
	toggle_off('Methods');
	toggle_on('Downloads');
	toggle_off('LATs');
	toggle_off('CATs');
	toggle_off('CLATs');
	toggle_off('Choose_Study');
  });

  $('#btn-close-transcript').click(function() { toggle_off('div-selected-transcripts'); });

});
