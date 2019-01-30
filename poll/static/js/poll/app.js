$(document).ready(function () {
    $('html').attr('lang')

    $('.carousel').carousel({
        interval: 5000 //changes the speed
    });

    maleGraphic('#column_chart');
    maleGraphic('#line_chart');

    set_tooltios();

    $('.datepicker').datepicker({
        zIndexOffset: 2000,
        language: LANGUAGE_CODE,
        endDate: new Date(),
        autoclose: true
    });
    // $('.edit-form').click(function () {
    //     $('form').find('input, textarea, button, select').attr('disabled', false);
    // })
});