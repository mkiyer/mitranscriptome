requirejs.config({
    urlArgs: "bust=" +  (new Date()).getTime(), 
    baseUrl: "/static/scripts",
    waitSeconds: 200,     
	  enforceDefine: true,

    paths: {
        'jquery': 'libs/jquery-1.11.1.min',
        'underscore': 'libs/underscore-min',
        'backbone': 'libs/backbone-min',
        'd3': 'libs/d3.v3.min',
        'bootstrap': '../bootstrap/js/bootstrap.min',
        'selectize': 'libs/selectize.min',
        'domReady': 'libs/domReady',
        'text': 'libs/text',
        'spin': 'libs/spin.min',
        'jqueryspin': 'libs/jquery.spin',
        'tablesorter': 'libs/jquery.tablesorter.min',
        'tablesorter.widgets': 'libs/jquery.tablesorter.widgets.min',
        'datatables': '../datatables/js/jquery.dataTables.min',
        'datatables.bootstrap': '../datatables/js/dataTables.bootstrap.min'
    },
    
    shim: {
        "underscore": {
            deps: [],
            exports: "_"
        },
        "backbone": {
            deps: ["jquery", "underscore"],
            exports: "Backbone"
        },
        'd3': {
        	deps: [],
        	exports: 'd3'
        },
        'bootstrap': {
            deps: ['jquery'],
            exports: "$.fn.popover"
        },
        'tablesorter': {
            deps: ['jquery'],
            exports: '$.fn.tablesorter'
        },
        'tablesorter.widgets': {
          deps: ['jquery', 'tablesorter'],
          exports: '$.tablesorter.themes.bootstrap'
        },
        'jqueryspin': {
          deps: ['spin', 'jquery'],
          exports: '$.fn.spin'
        }
    }    
});

require(['domReady'], function (domReady) {
  domReady(function () {
	//This function is called once the DOM is ready.
	//It will be safe to query the DOM and manipulate
	//DOM nodes in this function.
	console.log('DOM is ready');
    require(['app'], function() { console.log('APP'); });
  });
});

define(["jquery", "underscore", "backbone", 'd3', 'bootstrap', 'tablesorter', 'datatables', 'datatables.bootstrap'],
    function ($, _, Backbone, d3) {
        console.log("Test output");
        console.log("$: " + typeof $);
        console.log("_: " + typeof _);
        console.log("Backbone: " + typeof Backbone);
        console.log('d3: ' + typeof d3);
    }
);
