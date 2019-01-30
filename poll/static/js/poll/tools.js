function graphic(url, query_string, html) {
    var $char = null;
    if (url) {
        $.getJSON(url + '?' + query_string, function (data) {
            $char = $(html).highcharts(data);
        });
        return $char
    }
}

function maleGraphic(selector) {
    var $char = $(selector);
    return graphic($char.data('url'), 'username=' + $char.data('username'), selector);
}

function set_tooltios() {
    $('tbody .tooltip-td-options').each(function () {
        var $tooltipHide = $(this).find('.tooltip-hide');
        $(this).find('.tooltip-options').tooltip({
            title: $tooltipHide.html(),
            html: true,
            placement: "top"
        });
        $tooltipHide.remove();
    });
}