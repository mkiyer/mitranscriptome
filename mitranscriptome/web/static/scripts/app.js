define([
  'jquery',
  'underscore',
  'backbone',
  'd3',
  'collections/transcripts',
  'views/transcript_table',
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

  // application control logic
  $('#btn-aml').click(function() { 
	  console.log('AML'); 
	  transcriptTableView.load('aml');
  });

  $('#btn-bladder').click(function() { 
	  console.log('BLADDER'); 
	  transcriptTableView.load('bladder');
  });
  
  $('#btn-breast').click(function() { 
	  console.log('BREAST');
	  transcriptTableView.load('breast');
  });
 
  $('#btn-cervical').click(function() { 
	  console.log('CERVICAL'); 
	  transcriptTableView.load('cervical');
  });
  
  $('#btn-cml').click(function() { 
	  console.log('cml'); 
	  transcriptTableView.load('cml');
  });
  
  $('#btn-colorectal').click(function() { 
	  console.log('COLORECTAL'); 
	  transcriptTableView.load('colorectal');
  });
  
  $('#btn-gbm').click(function() { 
	  console.log('GBM'); 
	  transcriptTableView.load('gbm');
  });
  
  $('#btn-head_neck').click(function() { 
	  console.log('HEAD_NECK'); 
	  transcriptTableView.load('head_neck');
  });
  
  $('#btn-heart').click(function() { 
	  console.log('HEART'); 
	  transcriptTableView.load('heart');
  });
  
  $('#btn-hesc').click(function() { 
	  console.log('HESC'); 
	  transcriptTableView.load('hesc');
  });
  
  $('#btn-kich').click(function() { 
	  console.log('KICH'); 
	  transcriptTableView.load('kich');
  });
  
  $('#btn-kirc').click(function() { 
	  console.log('KIRC'); 
	  transcriptTableView.load('kirc');
  });
  
  $('#btn-kirp').click(function() { 
	  console.log('KIRP'); 
	  transcriptTableView.load('kirp');
  });
  
  $('#btn-lgg').click(function() { 
	  console.log('LGG'); 
	  transcriptTableView.load('lgg');
  });
  
  $('#btn-liver').click(function() { 
	  console.log('LIVER'); 
	  transcriptTableView.load('liver');
  });
  
  $('#btn-luad').click(function() { 
	  console.log('LUAD'); 
	  transcriptTableView.load('luad');
  });
  
  $('#btn-lusc').click(function() { 
	  console.log('LUSC'); 
	  transcriptTableView.load('lusc');
  });
  
  $('#btn-medulloblastoma').click(function() { 
	  console.log('MEDULLOBLASTOMA'); 
	  transcriptTableView.load('medulloblastoma');
  });
  
  $('#btn-melanoma').click(function() { 
	  console.log('MELANOMA'); 
	  transcriptTableView.load('melanoma');
  });
  
  $('#btn-mpn').click(function() { 
	  console.log('MPN'); 
	  transcriptTableView.load('mpn');
  });
  
  $('#btn-ovarian').click(function() { 
	  console.log('OVARIAN'); 
	  transcriptTableView.load('ovarian');
  });
  
  $('#btn-pancreatic').click(function() { 
	  console.log('PANCREATIC'); 
	  transcriptTableView.load('pancreatic');
  });
  
  $('#btn-prostate').click(function() { 
	  console.log('PROSTATE'); 
	  transcriptTableView.load('prostate');
  });
  
  $('#btn-skeletal_muscle').click(function() { 
	  console.log('SKELETAL_MUSCLE'); 
	  transcriptTableView.load('skeletal_muscle');
  });
  
  $('#btn-stomach').click(function() { 
	  console.log('STOMACH'); 
	  transcriptTableView.load('stomach');
  });
  
  $('#btn-thyroid').click(function() { 
	  console.log('THYROID'); 
	  transcriptTableView.load('thyroid');
  });
  
  $('#btn-uterine').click(function() { 
	  console.log('UTERINE'); 
	  transcriptTableView.load('uterine');
  });
  
  $('#btn-hiclinc').click(function() { 
	  console.log('HICLINC'); 
	  transcriptTableView.load('hiclinc');
  });

})
