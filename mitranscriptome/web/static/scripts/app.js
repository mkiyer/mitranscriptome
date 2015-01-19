define([
  'jquery',
  'underscore',
  'backbone',
  'd3',
  'text!jstemplates/ucsc_link.html',
  'text!jstemplates/transcript_details.html',
  'jqueryspin'
], function($, _, Backbone, d3,
    UCSCLinkTemplateText,
    TranscriptDetailsTemplateText) {

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
      if (data == 'Cancer') {
        return '<span class="label label-success">C</span>'
      } else if (data == 'Lineage') {
        return '<span class="label label-warning">L</span>'
      } else if (data == 'Cancer / Lineage') {
        return '<span class="label label-success">C</span>&nbsp;<span class="label label-warning">L</span>'
      } else {
        return '<span class="label label-default">NA</span>'
      }
    } else {
      return data;
    }
  }
  
  // map tissue codes to user-friendly names
  tissueMap = d3.map({
    aml: 'Blood / AML',
    bladder: 'Bladder',
    breast: 'Breast',
    cervical: 'Cervical',
    cml: 'Blood / CML',
    colorectal: 'Colorectal',
    gbm: 'Brain / Glioblastoma',
    head_neck: 'Head/Neck',
    heart: 'Muscle / Heart',
    embryonic_stem_cells: 'Embryonic Stem Cells',
    kich: 'Renal / Chromophobe',
    kirc: 'Renal / Clear Cell',
    kirp: 'Renal / Papillary',
    lgg: 'Brain / Glioma',
    liver: 'Liver',
    luad: 'Lung Adenocarcinoma',
    lusc: 'Lung Squamous',
    medulloblastoma: 'Brain / Medulloblastoma',
    melanoma: 'Melanoma',
    mpn: 'Blood / MPN',
    ovarian: 'Ovarian',
    pancreatic: 'Pancreatic',
    prostate: 'Prostate',
    skeletal_muscle: 'Muscle / Skeletal',
    stomach: 'Stomach',
    thyroid: 'Thyroid',
    uterine: 'Uterine',
    NA: 'NA'    
  });
  
  // transcript table (DataTable)
  var table = $('#table-transcripts')
    .on('preXhr.dt', function(e, settings, data) {
      $('#div-panel-load').spin();
    })
    .on('xhr.dt', function(e, settings, json) {
      $('#div-panel-load').spin(false);
      $('#btn-get-started').text('Click to browse transcripts');
      $('#btn-get-started').prop('disabled', false);
    })
    .DataTable({
    processing: false,
    deferRender: true,
    ajax: {
      url: '/transcript_metadata'
    },
    "order": [[1, 'asc']],
    columns: [
      {
        className: 'details-control',
        orderable: false,
        data: null,
        defaultContent: ''
      },
      { 
        data: "func_name_final" 
      },
      { 
        data: null,
        render: function(data, type, row, meta) {
          return UCSCLinkTemplate({row: row});
        }
      },
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
      { 
        // association type
        orderable: false,
        data: function(row, type, val, meta) {
          switch(row.association_type) {
            case 'c': return 'Cancer'; break;
            case 'l': return 'Lineage'; break;
            case 'cl': return 'Cancer / Lineage'; break;
            default: return 'NA'
          }
        },
        render: function(data, type, row, meta) {
          return associationRender(data,type);
        }
      },
      { 
        // tissue
        orderable: false,
        data: function(row, type, val, meta) {
          return tissueMap.get(row.tissue);
        }
      },      
      { 
        // ssea_percentile
        data: function(row, type, val, meta) {
          return (100 * (row.ssea_percentile == 'NA' ? 0.0 : parseFloat(row.ssea_percentile))).toFixed(2);
        },
        render: function(data, type, row, meta) {
          if (data > 0) {
            return '<span class="glyphicon glyphicon-arrow-up red"/>' + data;
          } else if (data < 0) {
            return '<span class="glyphicon glyphicon-arrow-down blue"/>' + data;
          } else {
            return data;
          }
        }
      },
      { 
        // tissue_expr_mean
        data: function(row, type, val, meta) { 
          return row.tissue_expr_mean == 'NA' ? 0.0 : parseFloat(row.tissue_expr_mean);
        } 
      },
      { 
        // tissue_expr_95
        data: function(row, type, val, meta) { 
          return row.tissue_expr_95 == 'NA' ? 0.0 : parseFloat(row.tissue_expr_95);
        }
      },
      { 
        // tissue_expr_99
        data: function(row, type, val, meta) { 
          return row.tissue_expr_99 == 'NA' ? 0.0 : parseFloat(row.tissue_expr_99);
        }
      }
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
  
  $('#div-transcript-browser').tooltip({ 
    delay: { show: 50, hide: 50 },
    selector:"[data-toggle=tooltip]"
  });

  // home button functionality
  $('#btn-home').click(function() {
    $('#div-welcome').show();
    $('#div-transcript-browser').hide();
//    // this is unfortunately hard-coded due to nature of DataTables
//    table.rows().indexes().flatten().each( function ( i ) {
//      var row = table.row( i );
//      if ( row.child.isShown() ) {
//        // This row is already open - close it
//        row.child.hide();
//        row.nodes().to$().removeClass('shown');
//      }
//    });
  });
  
  // get started button functionality
  $('#btn-get-started').click(function() {
    $('#div-welcome').hide();
    $('#div-transcript-browser').show();
  });
})
