from django.conf.urls import patterns, url

from poll.views import charts, views, admin

# USER = '(?P<username>([0-9]|[a-z]|[A-Z])+)'

urlpatterns = [
    url(r'^questionnaire/$', views.QuestionnaireView.as_view(), name='questionnaire'),
    url(r'^update_polldate_score/$', views.UpdatePollDateScore.as_view(), name='update_polldate_score'),
    url(r'^score/$', charts.ScoreView.as_view(), name='score'),
    url(r'^graphic/$', charts.GBarView.as_view(), name='graphic'),
    url(r'^practice_score_column_chart/$', charts.PracticeScoreColumnChart.as_view(), name='practice_score_column_chart'),
    url(r'^question_line_chart/$', charts.QuestionLineChart.as_view(), name='question_line_chart'),
    url(r'^poll_date_bar_chart/$', charts.PollDateBarChart.as_view(), name='poll_date_bar_chart'),
    url(r'^poll_date_line_chart/$', charts.PollDateLineChart.as_view(), name='poll_date_line_chart'),
    url(r'^question_bar_chart/$', charts.QuestionBarChart.as_view(), name='question_bar_chart'),
    url(r'^poll_list/$', views.PollListView.as_view(), name='poll_list'),

    url(r'^demographics/$', views.DemographicsFormView.as_view(), name='demographics'),

    # admin json views
    url(r'^answers_by_user_json_view/$', admin.AnswersByUserJsonView.as_view(), name='answers_by_user_json_view'),
    url(r'^questionnaire/(?P<poll>[-\w]+)/$', views.QuestionnaireView.as_view(), name='questionnaire'),
]
