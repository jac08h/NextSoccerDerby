$(document).ready(function() {
  $('#fixtures_table').DataTable({
    "ajax": {
      "url": "/fixtures",
      "type": "POST"
    },
    "columns": [
    { "data": "title"},
    { "data": "date"},
    { "data": "teams"},
    { "data": "competition"},
    { "data": "country"},

    { "data": "country"}  // placeholder
    ],
    "order": [
      [1, "asc"]
    ],

    "responsive": {
      "details": {
        "renderer": function(api, rowIdx, columns) {
          // Show hidden columns in row details
          var data = $.map(columns, function(col, i) {
            if(i == 5){ return; }
            return col.hidden ?
              '<tr><td>' + col.title + ':</td> ' +
              '<td>' + col.data + '</td></tr>' :
              '';
          }).join('');

          // Generate a table
          data = $('<table width="100%"/>').append(data).prop('outerHTML');

          return data;
        }
      }
    },
    "scrollY": "50vh",
    "scrollCollapse": true,
    "paging": false,
    "columnDefs": [
        // not displayed directly, only upon clicking on '+' button
        {
            "className": 'none',
            "targets": [ 3, 4 ]
        },

        // placeholder to always display '+' button
        {
            "className": 'none',
            "targets": [ 5 ]
        }
        ],

    "language": {
        "emptyTable": "No matches with known date available.",
    }

  });
})