/**
 * Created by leon on 19/08/16.
 */
$(document).ready(function () {
    /* for admin pull page */
    var $charLine = $('#line-chart-poll');
    var $charBar = $('#column-chart-poll');

    $('#update_score').click(function () {
        $.get($(this).data('url'), {
            poll_id: $(this).data('poll'),
            update_score_practice: "1",
            update_score_question: "1"
        }).done(function (data) {
            location.reload($(this).attr('href'));
        });
    });

    graphic($charBar.data('url'), "poll_id=" + $charBar.data('poll'), "#column-chart-poll");
    graphic($charLine.data('url'), "poll_id=" + $charLine.data('poll'), "#line-chart-poll");

    /* for admin respondent page */
    maleGraphic('#column-chart-respondent-admin');
    maleGraphic('#line-chart-respondent-admin');

    $("#polldate_set-group .vDateField").datepicker({
        zIndexOffset: 2000,
        language: LANGUAGE_CODE,
        autoclose: true
    });

    $("#demographics-group .vDateField").datepicker({
        zIndexOffset: 2000,
        language: LANGUAGE_CODE,
        endDate: new Date(),
        autoclose: true
    });


    /* for admin question page */
    var chartQuestion = $('#column-chart-question-admin');
    graphic(chartQuestion.data('url'), "question_id=" + chartQuestion.data('question'), '#column-chart-question-admin');

});
