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
 // selectedTranscripts.load('breast');
 
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
  $('#Select_Transcripts_Btn').click(function() {
	toggle_off('Home');
	toggle_off('Methods');
	toggle_off('Downloads');
	toggle_on('Select_Transcripts');
	toggle_off('LATs');
	toggle_off('CATs');
	toggle_off('CLATs');
	toggle_off('HiCLNCs')
	toggle_off('Annotated')
  });
  $('#Methods_Btn').click(function() {
	toggle_off('Home');
	toggle_on('Methods');
	toggle_off('Downloads');
	toggle_off('Select_Transcripts');
	toggle_off('LATs');
	toggle_off('CATs');
	toggle_off('CLATs');
	toggle_off('HiCLNCs')
	toggle_off('Annotated')
  });
  $('#Downloads_Btn').click(function() {
	toggle_off('Home');
	toggle_off('Methods');
	toggle_on('Downloads');
	toggle_off('LATs');
	toggle_off('CATs');
	toggle_off('CLATs');
	toggle_off('Select_Transcripts');
	toggle_off('HiCLNCs')
	toggle_off('Annotated')
  });

  $('#btn-close-transcript').click(function() { toggle_off('div-selected-transcripts'); });
 
  $('#btn-aml').click(function() { 
	  console.log('AML'); 
	  selectedTranscripts.load('aml');
  });

  $('#btn-bladder').click(function() { 
	  console.log('BLADDER'); 
	  selectedTranscripts.load('bladder');
  });
  
  $('#btn-breast').click(function() { 
	  console.log('BREAST'); 
	  selectedTranscripts.load('breast');
  });
 
  $('#btn-cervical').click(function() { 
	  console.log('CERVICAL'); 
	  selectedTranscripts.load('cervical');
  });
  
  $('#btn-cml').click(function() { 
	  console.log('cml'); 
	  selectedTranscripts.load('cml');
  });
  
  $('#btn-colorectal').click(function() { 
	  console.log('COLORECTAL'); 
	  selectedTranscripts.load('colorectal');
  });
  
  $('#btn-gbm').click(function() { 
	  console.log('GBM'); 
	  selectedTranscripts.load('gbm');
  });
  
  $('#btn-head_neck').click(function() { 
	  console.log('HEAD_NECK'); 
	  selectedTranscripts.load('head_neck');
  });
  
  $('#btn-heart').click(function() { 
	  console.log('HEART'); 
	  selectedTranscripts.load('heart');
  });
  
  $('#btn-hesc').click(function() { 
	  console.log('HESC'); 
	  selectedTranscripts.load('hesc');
  });
  
  $('#btn-kich').click(function() { 
	  console.log('KICH'); 
	  selectedTranscripts.load('kich');
  });
  
  $('#btn-kirc').click(function() { 
	  console.log('KIRC'); 
	  selectedTranscripts.load('kirc');
  });
  
  $('#btn-kirp').click(function() { 
	  console.log('KIRP'); 
	  selectedTranscripts.load('kirp');
  });
  
  $('#btn-lgg').click(function() { 
	  console.log('LGG'); 
	  selectedTranscripts.load('lgg');
  });
  
  $('#btn-liver').click(function() { 
	  console.log('LIVER'); 
	  selectedTranscripts.load('liver');
  });
  
  $('#btn-luad').click(function() { 
	  console.log('LUAD'); 
	  selectedTranscripts.load('luad');
  });
  
  $('#btn-lusc').click(function() { 
	  console.log('LUSC'); 
	  selectedTranscripts.load('lusc');
  });
  
  $('#btn-medulloblastoma').click(function() { 
	  console.log('MEDULLOBLASTOMA'); 
	  selectedTranscripts.load('medulloblastoma');
  });
  
  $('#btn-melanoma').click(function() { 
	  console.log('MELANOMA'); 
	  selectedTranscripts.load('melanoma');
  });
  
  $('#btn-mpn').click(function() { 
	  console.log('MPN'); 
	  selectedTranscripts.load('mpn');
  });
  
  $('#btn-ovarian').click(function() { 
	  console.log('OVARIAN'); 
	  selectedTranscripts.load('ovarian');
  });
  
  $('#btn-pancreatic').click(function() { 
	  console.log('PANCREATIC'); 
	  selectedTranscripts.load('pancreatic');
  });
  
  $('#btn-prostate').click(function() { 
	  console.log('PROSTATE'); 
	  selectedTranscripts.load('prostate');
  });
  
  $('#btn-skeletal_muscle').click(function() { 
	  console.log('SKELETAL_MUSCLE'); 
	  selectedTranscripts.load('skeletal_muscle');
  });
  
  $('#btn-stomach').click(function() { 
	  console.log('STOMACH'); 
	  selectedTranscripts.load('stomach');
  });
  
  $('#btn-thyroid').click(function() { 
	  console.log('THYROID'); 
	  selectedTranscripts.load('thyroid');
  });
  
  $('#btn-uterine').click(function() { 
	  console.log('UTERINE'); 
	  selectedTranscripts.load('uterine');
  });
  
  $('#btn-hiclinc').click(function() { 
	  console.log('HICLINC'); 
	  selectedTranscripts.load('hiclinc');
  });
  
  
//  $('#btn-breast').click(function() { 
//	  console.log('BREAST'); 
//	  selectedTranscripts.load('breast');
//  });
//  var val = $("#myOptions option:selected").text();
  
})
