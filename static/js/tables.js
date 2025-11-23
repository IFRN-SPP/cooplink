$(document).ready(function() {
  $('#ajax-table').each(function() {
    var table = $(this);
    var tableType = table.data('type');

    function parseDate(dateStr) {
      if (!dateStr) return 0;
      
      var parts = dateStr.split(' ')[0].split('/');
      if (parts.length === 3) {
        var day = parseInt(parts[0], 10);
        var month = parseInt(parts[1], 10) - 1;
        var year = parseInt(parts[2], 10);
        
        var timeParts = dateStr.split(' ')[1]?.split(':') || ['00', '00'];
        var hours = parseInt(timeParts[0], 10) || 0;
        var minutes = parseInt(timeParts[1], 10) || 0;
        
        return new Date(year, month, day, hours, minutes).getTime();
      }
      
      return new Date(dateStr).getTime() || 0;
    }

    $.fn.dataTable.ext.type.order['date-br-pre'] = parseDate;

    var getDynamicColumnsConfig = function(table, tableType) {
      var columnCount = table.find('thead th').length;
      
      var configs = {
        'order': [
          { "orderable": true, "targets": [0] },
          { "orderable": false, "targets": [columnCount - 1] },
          ...(columnCount === 6 ? [
            { "orderable": true, "targets": [1, 2] },
            { "orderable": false, "targets": [3] },
            { "targets": [4], "type": "date-br" }
          ] : columnCount === 5 ? [
            { "orderable": true, "targets": [1] },
            { "orderable": false, "targets": [2] },
            { "targets": [3], "type": "date-br" }
          ] : []),
        ],
        'call': [
          { "orderable": true, "targets": [0] },
          { "orderable": false, "targets": [columnCount - 1] },
          ...(columnCount === 6 ? [
            { "orderable": true, "targets": [1] },
            { "targets": [2, 3], "type": "date-br" },
            { "orderable": false, "targets": [4] }
          ] : columnCount === 5 ? [
            { "targets": [1, 2], "type": "date-br" },
            { "orderable": false, "targets": [3] }
          ] : []),
        ],
        'institution': [
          { "orderable": true, "targets": [0, 1] },
          { "orderable": false, "targets": [2, 3] }
        ],
        'product': [
          { "orderable": true, "targets": [0, 1] },
          { "orderable": false, "targets": [2, 3] }
        ],
        'user': [
          { "orderable": true, "targets": [0, 1, 2, 3] },
          { "orderable": false, "targets": [4, 5, 6] }
        ]
      };

      return configs[tableType] || [];
    };

    var columnsConfig = getDynamicColumnsConfig(table, tableType);

    var dataTable = table.DataTable({
      "order": [[0, "desc"]],
      "pageLength": 6,
      "lengthChange": false,
      "paging": false,
      "info": false,
      "searching": true,
      "language": {
        "url": "https://cdn.datatables.net/plug-ins/2.0.0/i18n/pt-BR.json"
      },
      "columnDefs": columnsConfig,
      colReorder: true,
      dom: '<"top"fB>rt',
      buttons: [{
        extend: 'colvis',
        text: 'FILTRAR COLUNAS',
        className: 'btn btn-outline-success',
        columns: ':not(:last-child)',
        columnText: function ( dt, idx, title ) {
            var th = $(dt.column(idx).header());
            var columnTitle = th.find('.dt-column-title').clone().children().remove().end().text().trim();
            return columnTitle || th.find('.dt-column-title').text().split('\n')[0].trim();
          }
        }
      ],
      initComplete: function() {
        $('div.dt-search label').remove();
        $('div.dt-search input').attr('placeholder', 'Buscar...');
      }
    });

    var filters = {
      institution: '',
      author: '',
      status: [],
      situation: [], 
      unit: [],
    };

    function hasActiveFilters(filterArray) {
      return filterArray && filterArray.length > 0;
    }

    function updateFilterIndicator(icon, filterArray) {
      if (hasActiveFilters(filterArray)) {
        icon.addClass('filter-active');
      } else {
        icon.removeClass('filter-active');
      }
    }

    function checkDateFilter(dateStr) {
      if (!dateStr) return true;
      
      var datePart = dateStr.split(' ')[0];
      var parts = datePart.split('/');
      
      if (filters.day && parts[0] !== filters.day) return false;
      if (filters.month && parts[1] !== filters.month) return false;
      if (filters.year && parts[2] !== filters.year) return false;
      
      return true;
    }

    $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
      var row = $(dataTable.row(dataIndex).node());
      
      var institution = row.find('td.institution-column').data('institution');
      if (filters.institution && institution !== filters.institution) return false;
      
      var author = row.find('td.author-column').data('author');
      if (filters.author && author !== filters.author) return false;
      
      var status = row.find('td.status-column').data('status');
      if (filters.status.length && !filters.status.includes(status)) return false;
      
      var unit = row.find('td.unit-column').data('unit');
      if (filters.unit.length && !filters.unit.includes(unit)) return false;
      
      var situation = row.find('td.situation-column').data('situation');
      if (filters.situation.length && !filters.situation.includes(situation.toString())) return false;

      return true;
    });

    table.on('click', 'td.institution-column, td.author-column', function() {
      var type = $(this).hasClass('institution-column') ? 'institution' : 'author';
      var val = $(this).data(type);
      filters[type] = (filters[type] === val ? '' : val);
      dataTable.draw();
    });

    $('.status-checkbox, .situation-checkbox, .unit-checkbox').on('change', function() {
      var type = $(this).hasClass('status-checkbox') ? 'status' : 
                 $(this).hasClass('situation-checkbox') ? 'situation' : 'unit';
      
      filters[type] = $('.' + type + '-checkbox:checked').map(function() {
        return $(this).val();
      }).get();
      
      if (type === 'status') {
        updateFilterIndicator($('#status-filter-icon'), filters.status);
      } else if (type === 'situation') {
        updateFilterIndicator($('#situation-filter-icon'), filters.situation);
      } else if (type === 'unit') {
        updateFilterIndicator($('#unit-filter-icon'), filters.unit);
      }
      
      dataTable.draw();
    });

    $('th').each(function() {
      var th = $(this);
      var thText = th.text();
      
      if (thText.includes('STATUS')) {
        th.find('.dropdown a').attr('id', 'status-filter-icon');
      } else if (thText.includes('SITUAÇÃO')) {
        th.find('.dropdown a').attr('id', 'situation-filter-icon');
      } else if (thText.includes('UNIDADE') || thText.includes('UNIT')) {
        th.find('.dropdown a').attr('id', 'unit-filter-icon');
      }
    });
  });
});
