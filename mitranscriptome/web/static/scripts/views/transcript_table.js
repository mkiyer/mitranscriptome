define([
  'jquery', 
  'underscore', 
  'backbone',
  'text!jstemplates/transcript_table.html',
  'collections/transcripts',
  'tablesorter',
  'tablesorter.widgets',
  'jqueryspin'
], function($, _, Backbone,
  TranscriptTableTemplate,
  TranscriptCollection) {
  
  // adjust bootstrap table theme
  $.extend($.tablesorter.themes.bootstrap, {
    // these classes are added to the table. To see other table classes available,
    // look here: http://twitter.github.com/bootstrap/base-css.html#tables
    table      : 'table table-bordered',
    caption    : 'caption',
    header     : 'bootstrap-header', // give the header a gradient background
    footerRow  : '',
    footerCells: '',
    icons      : '', // add "icon-white" to make them white; this icon class is added to the <i> in the header
    sortNone   : 'bootstrap-icon-unsorted',
    sortAsc    : 'icon-chevron-up glyphicon glyphicon-chevron-up',     // includes classes for Bootstrap v2 & v3
    sortDesc   : 'icon-chevron-down glyphicon glyphicon-chevron-down', // includes classes for Bootstrap v2 & v3
    active     : '', // applied when column is sorted
    hover      : '', // use custom css here - bootstrap class may not override it
    filterRow  : '', // filter row class
    even       : '', // odd row zebra striping
    odd        : ''  // even row zebra striping
  });
  
  // define view
  var TranscriptTableView = Backbone.View.extend({

    initialize: function(options) {
      var self = this;
      // attributes
      self.template = _.template(TranscriptTableTemplate);
      // register events
      // bind view to collection
      self.listenTo(self.collection, 'sync', self.render);
    },

    load: function(func_type) {
      var self = this;
      // show loading spinner
      self.$el.spin();
      // clear collection
      self.collection.reset();
      // update ajax parameters
      _.extend(self.collection.ajaxParams,
        { data: JSON.stringify({ func_type: func_type }) }
      );
      // trigger asynchronous load of new data (will call render() when done)
      self.collection.fetch(self.collection.ajaxParams);
    },

    render: function() {
      var self = this;
      // turn off loading spinner
      self.$el.spin(false);
      // render the collection to html
      self.$el.html(self.template({ 'transcriptCollection': self.collection }));
      // add tablesorter functionality to table
      $('#transcripts_table').tablesorter({
        theme: 'bootstrap',
        widthFixed: true,
        headerTemplate : '{content} {icon}',
        widgets : ["uitheme"],
      });
      return self;
    }

  });

  return TranscriptTableView;
});

