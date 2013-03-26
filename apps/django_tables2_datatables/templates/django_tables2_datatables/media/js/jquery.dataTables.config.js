//params
var table_class = '{{ datatable_table_class }}';

var filter_table_find_attr = '{{ datatable_filter_table_find_attr }}';
var filter_table_regex_attr = '{{ datatable_filter_table_regex_attr }}';
var filter_table_smart_attr = '{{ datatable_filter_table_smart_attr }}';

var filter_col_find_attr = '{{ datatable_filter_col_find_attr }}';
var filter_col_regex_attr = '{{ datatable_filter_col_regex_attr }}';
var filter_col_smart_attr = '{{ datatable_filter_col_smart_attr }}';

var filter_html_class = '{{ datatable_filter_html_class }}';
var filter_checkbox_class = '{{ datatable_filter_checkbox_class }}';

//filters table with given table_id globally
function fnFilterGlobal ( table_id )
{

    $('#'+table_id).dataTable().fnFilter(

        $('body').find(
          '['+filter_table_find_attr+'='+table_id+']' 
        ).val(),

        null,

        $('body').find(
          '['+filter_table_regex_attr+'='+table_id+']' 
        )[0].checked,

        $('body').find(
          '['+filter_table_smart_attr+'='+table_id+']' 
        )[0].checked

    );
}

//filters table with given table_id globally according to column i
//TODO broken
function fnFilterColumn ( table_id, i )
{
    $('#'+table_id).dataTable().fnFilter(

        $('body').find(
          '.'+datatable_global_filter_class
        ).filter(
          '['+datatable_filter_target_table_attr+'='+table_id+']' 
        ).filter(
          '['+datatable_filter_target_col_attr+'='+i+']' 
        ).val(),

        i,

        $('body').find(
          '.'+datatable_global_regex_class
        ).filter(
          '['+datatable_filter_target_table_attr+'='+table_id+']' 
        ).filter(
          '['+datatable_filter_target_col_attr+'='+i+']' 
        )[0].checked,

        $('body').find(
          '.'+datatable_global_smart_class
        ).filter(
          '['+datatable_filter_target_table_attr+'='+table_id+']' 
        ).filter(
          '['+datatable_filter_target_col_attr+'='+i+']' 
        )[0].checked
    );
}

//dom sorting

    //sort checkboxes
    //http://datatables.net/examples/plug-ins/dom_sort.html
    $.fn.dataTableExt.afnSortData['dom-checkbox'] = function  ( oSettings, iColumn )
    {
      var aData = [];
      $( 'td:eq('+iColumn+') input', oSettings.oApi._fnGetTrNodes(oSettings) ).each( function () {
        aData.push( this.checked==true ? "1" : "0" );
      } );
      return aData;
    }

    //$.fn.dataTableExt.ofnSearch['html'] = function ( sData ) {
        //var n = document.createElement('div');
        //n.innerHTML = sData;
        //if ( n.textContent ) {
            //return n.textContent.replace(/\n/g," ");
        //} else {
            //return n.innerText.replace(/\n/g," ");
        //}
    //}

    //sort text boxes
    //$.fn.dataTableExt.afnSortData['dom-text'] = function  ( oSettings, iColumn )
    //{
      //var aData = [];
      //$( 'td:eq('+iColumn+') input', oSettings.oApi._fnGetTrNodes(oSettings) ).each( function () {
        //aData.push( this.value );
      //} );
      //return aData;
    //}

    //sort select boxes
    //$.fn.dataTableExt.afnSortData['dom-select'] = function  ( oSettings, iColumn )
    //{
      //var aData = [];
      //$( 'td:eq('+iColumn+') select', oSettings.oApi._fnGetTrNodes(oSettings) ).each( function () {
        //aData.push( $(this).val() );
      //} );
      //return aData;
    //}

//html filtering
    $.fn.dataTableExt.ofnSearch[filter_html_class] = function ( sData ) {
      return sData.replace(/\n/g," ").replace( /<.*?>/g, "" );
    }
 
$(document).ready(function() 
{ 

    var oTable = $('.'+table_class).dataTable( {
            "oLanguage": {
                "sSearch": "search all: ",
                "sLengthMenu": "entries per page: _MENU_",
                "sZeroRecords": "no entries",
                "sInfo": "_START_ to _END_ of _TOTAL_ downloaded",
                "sInfoEmpty": "0 to 0 of 0",
                //"sInfoFiltered": "(filtered from _MAX_ total records)"
            },

            "aoColumnDefs": [
              //{ "sSortDataType": "dom-text", "aTargets": [ 'text' ] },
              //{ "sSortDataType": "dom-text", "sType": "numeric", "aTargets": [ 'text' ] },
              //{ "sSortDataType": "dom-select", "aTargets": [ 'select' ] },
              { "aTargets": [ filter_checkbox_class ], "sSortDataType": "dom-checkbox" } ,
              { "aTargets": [ filter_html_class ], "sType": "html",
                //WORKAROUND 1.9.4 http://datatables.net/forums/discussion/179/searchfilter-finds-matches-in-html-tags/p1
                  //sType broken for filtering
                  "mRender":function (data, type, full) { return (type == 'filter' ? data.replace(/<[^>]+>/g, '') : data); }
              }
            ],
            //class or columns to act
            
            //"sDom": 'rt<"bottom"iflp<"clear">>', //order of elements
            "sDom": '<"top"><"clear">rt', //order of elements
            "iDisplayLength": -1,

            "aLengthMenu": [[10, 25, 50, 100, 1000, -1], [10, 25, 50, 100, 1000, "all" ]],
            //values on the lenght menu
            
            //scrolling
            "bScrollCollapse": true,
            "bScrollInfinite": true,
            //"sScrollX": "100%",
            //"sScrollXInner": "110%",
            
            'bAutoWidth': false,
            //dont fix widths
        } );

    //tfoot input filtering
        //oTable.find("tfoot input").keyup( function () {
            //oTable.fnFilter( this.value, $("tfoot td").index($(this).parent()) );
        //} );

        //oTable.find("tfoot input").each( function (i) {
            //asInitVals[i] = this.value;
        //} );
        
        //oTable.find("tfoot input").focus( function () {
            //if ( this.className == "search_init" )
            //{
                //this.className = "";
                //this.value = "";
            //}
        //} );
        
        //oTable.find("tfoot input").blur( function (i) {
            //if ( this.value == "" )
            //{
                //this.className = "search_init";
                //this.value = asInitVals[$("tfoot input").index(this)];
            //}
        //} );

    //separate input filtering
        //assumes that each filter, regex and smart is in the same column

        $("input[" + filter_table_find_attr  + "]" ).keyup( function() { fnFilterGlobal( $(this).attr(filter_table_find_attr) ); } );
        $("input[" + filter_table_regex_attr + "]" ).click( function() { fnFilterGlobal( $(this).attr(filter_table_regex_attr) ); } );
        $("input[" + filter_table_smart_attr + "]" ).click( function() { fnFilterGlobal( $(this).attr(filter_table_smart_attr) ); } );
        
        $("input[" + filter_col_find_attr  + "]" ).keyup( function() { fnFilterColumn( $(this).attr(datatable_filter_target_table_attr), $(this).attr(datatable_filter_target_col_attr) ); } );
        $("input[" + filter_col_regex_attr + "]" ).click( function() { fnFilterColumn( $(this).attr(datatable_filter_target_table_attr), $(this).attr(datatable_filter_target_col_attr) ); } );
        $("input[" + filter_col_smart_attr + "]" ).click( function() { fnFilterColumn( $(this).attr(datatable_filter_target_table_attr), $(this).attr(datatable_filter_target_col_attr) ); } );
}); 
