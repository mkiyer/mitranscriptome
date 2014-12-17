define([
  'jquery',
  'underscore',
  'backbone',
  'd3',
  'text!jstemplates/ucsc_link.html',
  'text!jstemplates/transcript_details.html',
  'collections/transcripts',
  'views/transcript_table',
  'selectize'
], function($, _, Backbone, d3,
    UCSCLinkTemplateText,
    TranscriptDetailsTemplateText,
    TranscriptCollection,
    TranscriptTableView) {

  // templates
  var UCSCLinkTemplate = _.template(UCSCLinkTemplateText);
  var TranscriptDetailsTemplate = _.template(TranscriptDetailsTemplateText);
  
  // function to render binary data as ok / error glyphicons
  function binaryRender(data, type, trueValue) {
    if (type == 'display') {
      return data == trueValue ?
          '<span class="glyphicon glyphicon-ok-circle green"/>' :
          '<span class="glyphicon glyphicon-remove-sign"/>';           
    } else {
      return data;
    }
  }
  function associationRender(data,type) {
    if (type == 'display') {
      if (data == 'c') {
        return '<span class="label label-success">C</span>'
      } else if (data == 'l') {
        return '<span class="label label-warning">L</span>'
      } else if (data == 'cl') {
        return '<span class="label label-success">C</span>&nbsp;<span class="label label-warning">L</span>'
      } else {
        return '<span class="label label-default">NA</span>'
      }
    } else {
      return data;
    }
  }

  
//  <div id="Select_Transcripts" class="jumbotron jumbothin">
//  <label for="select-transcripts"><h4>Select Tissue/Cancer Type:</h4></label>
//  <select id="select-transcripts">
//    <option value="">Cancer Type/Tissue Type</option>
//    <option value="aml">Acute Myelogenous Leukemia (AMATs)</option>
//    <option value="bladder">Bladder Cancer (BLCATs)</option>
//    <option value="breast">Breast Cancer (BRCATs)</option>
//    <option value="cervical">Cervical Cancer (CVATs)</option>
//    <option value="cml">Chronic Myelogenous Leukemia (CMATs)</option>
//    <option value="colorectal">Colorectal Cancer (CRATs)</option>
//    <option value="gbm">Glioblastoma Multiforme (GBATs)</option>
//    <option value="head_neck">Head and Neck Cancer (HNCATs)</option>
//    <option value="heart">Heart Tissue (HRATs)</option>
//    <option value="hesc">Human Embryonic Stem Cells (ESATs)</option>
//    <option value="kich">Chromophobe Renal Cell Carcinoma (KCHCATs)</option>
//    <option value="kirc">Renal Clear Cell Carcinoma (KCCATs)</option>
//    <option value="kirp">Renal Papillary Cell Carcinoma (KPCATs)</option>
//    <option value="lgg">Low Grade Glioma (LGATs)</option>
//    <option value="liver">Liver Cancer (LVCATs)</option>
//    <option value="luad">Lung Adenocarcinoma (LACATs)</option>
//    <option value="lusc">Lung Squamous Cell Carcinoma (LSCATs)</option>
//    <option value="medulloblastoma">Medulloblastoma (MBATs)</option>
//    <option value="melanoma">Melanoma (MEATs)</option>
//    <option value="mpn">Myeloproliferative Neoplasia (MPATs)</option>
//    <option value="ovarian">Ovarian Cancer (OVATs)</option>
//    <option value="pancreatic">Pancreatic Cancer (PNATs)</option>
//    <option value="prostate">Prostate Cancer (PCATs)</option>
//    <option value="skeletal_muscle">Skeletal Muscle Tissue (SMATs)</option>
//    <option value="stomach">Stomach Cancer (STCATs)</option>
//    <option value="thyroid">Thyroid Cancer (THCATs)</option>
//    <option value="uterine">Uterine Endometrial Carcinoma (UTATs)</option>
//    <option value="hiclinc">Highly Conserved Long Intergenic Non-Coding RNAs (HICLINCs)</option>
//  </select>
//</div><!-- /Select Transcripts -->
  
//  {
//    // unannotated/annotated
//    targets: 3,
//    orderable: false,
//    data: 'tstatus',
//    render: function(data, type, row, meta) {
//      return binaryRender(data, type, 'unannotated');
//    }
//  }, 

  // transcript table (DataTable)
  var table = $('#table-transcripts').DataTable({
    processing: true,
    deferRender: true,
    ajax: {
      url: '/transcript_metadata'
    },
    "order": [[1, 'asc']],
    columnDefs: [{
      // genome location
      targets: 2,
      data: null,
      render: function(data, type, row, meta) {
        return UCSCLinkTemplate({row: row});
      }
    }, {
      // Association Type
      targets: 7,
      orderable: false,
      data: 'association_type',
      render: function(data, type, row, meta) {
        return associationRender(data, type);
      }
    }],
    columns: [
      {
        "className": 'details-control',
        "orderable": false,
        "data": null,
        "defaultContent": ''
      },
      { data: "func_name_final" },
      { data: null },
      { 
        // tstatus (annotated / unannotated)
        orderable: false,
        data: function(row, type, val, meta) {
          return row.tstatus == 'annotated' ? 'YES' : 'NO';
        },
        render: function(data, type, row, meta) {
          return binaryRender(data, type, 'YES');
        }
      },
      { 
        // tgenic (intergenic / intragenic)
        orderable: false,
        data: function(row, type, val, meta) {
          return row.tgenic == 'intergenic' ? 'YES' : 'NO';
        },
        render: function(data, type, row, meta) {
          return binaryRender(data, type, 'YES');
        }
      },
      { 
        // tcat (lncrna / tucp)
        orderable: false,
        data: function(row, type, val, meta) {
          return row.tcat == 'tucp' ? 'TUCP' : 'lncRNA';
        }
      },
      {
        // uce (FALSE / TRUE)
        orderable: false,
        data: function(row, type, val, meta) {
          return row.uce == 'TRUE' ? 'YES' : 'NO';
        },
        render: function(data, type, row, meta) {
          return binaryRender(data, type, 'YES');
        }
      }, 
      { data: "association_type" },
      { 
        data: "tissue",
        orderable: false
      },
      { 
        // ssea_percentile
        data: function(row, type, val, meta) {
          return row.ssea_percentile == 'NA' ? 0.0 : parseFloat(row.ssea_percentile);
        }
      },
      { data: function(row, type, val, meta) { return parseFloat(row.tissue_expr_mean); } },
      { data: function(row, type, val, meta) { return parseFloat(row.tissue_expr_95); } },
      { data: function(row, type, val, meta) { return parseFloat(row.tissue_expr_99); } }
    ],
    initComplete: function () {
      var api = this.api();
      // need to specify "selectable" columns
      // this is unfortunately hard-coded due to nature of DataTables
      selectColumns = [3,4,5,6,7,8]
      selectColumns.forEach(function(i) {
      //api.columns().indexes().flatten().each( function ( i ) {
        var column = api.column( i );
        var select = $('<br/><select><option value=""></option></select>')
          .appendTo( $(column.header()) )
        //.appendTo( $(column.footer()).empty() )
          .on('change', function () {
            var val = $.fn.dataTable.util.escapeRegex( $(this).val() );
            column
              .search( val ? '^'+val+'$' : '', true, false )
              .draw();
          });
          column.data().unique().sort().each( function ( d, j ) {
            select.append( '<option value="'+d+'">'+d+'</option>' )
          });
      });
      // recalculate column widths
      api.columns.adjust().draw();
    }
  });
  
  // Add event listener for opening and closing details
  $('#table-transcripts tbody').on('click', 'td.details-control', function () {
      var tr = $(this).closest('tr');
      var row = table.row( tr );

      if ( row.child.isShown() ) {
          // This row is already open - close it
          row.child.hide();
          tr.removeClass('shown');
      }
      else {
          // Open this row
          row.child( TranscriptDetailsTemplate(row.data()) ).show();
          tr.addClass('shown');
      }
  });
  
  // add tooltip functionality
  $('#table-transcripts').tooltip({ 
    delay: { show: 100, hide: 100 },
    selector:"[data-toggle=tooltip]",
    container:"body"      
  });

  // get started button functionality
  $('#btn-get-started').click(function() {
    $('#div-welcome').hide();
    $('#div-transcript-browser').show();
  });

  // collections
  var selectedTranscripts = new TranscriptCollection;
  // views
  var transcriptTableView = new TranscriptTableView({ 
    el: '#div-transcript-table',
    collection: selectedTranscripts
  });

  // selectize control for tissue/cancer type
  $('#select-transcripts').selectize({
    onChange: function(value) {
      console.log(value);
      // trigger load of transcript table
      transcriptTableView.load(value);
      // show transcript table
      toggle_off('Home')
      $('#div-selected-transcripts').show();
    }
  });
  
  $('#select-transcripts2').selectize({
	    onChange: function(value) {
	      console.log(value);
	      // trigger load of transcript table
	      transcriptTableView.load(value);
	      // show transcript table
	      toggle_off('Home')
	      $('#div-selected-transcripts').show();
	    }
	  });

})
