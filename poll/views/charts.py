from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from poll.templatetags.poll_tag import distinct
from poll.models import Answer, PracticeScore, PollDate, Question, Respondent
from highcharts.views import HighChartsBarView
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count


class PracticeScoreColumnChart(HighChartsBarView):
    title = _(u'Practice Chart').format()
    chart_type = 'column'
    yAxis = {
        'allowDecimals': True,
        'tickInterval': 0.5,
        'max': 5.0,
    }
    tooltip = {
        'shared': True,
        'crosshairs': True,
    }

    def get_data(self):
        data = super(PracticeScoreColumnChart, self).get_data()
        data['xAxis']['categories'] = self.categories
        data['yAxis'] = self.yAxis
        data['tooltip'] = self.tooltip
        return data

    @property
    def series(self):
        username = self.request.GET.get('username', None)
        if not username:
            return ''
        user = User.objects.filter(username=username).first()
        practice_score = PracticeScore.objects.filter(respondent=user.respondent).order_by('practice__name',
                                                                                           'poll__order')
        self.categories = distinct([str(p.practice) for p in practice_score])
        result = []
        polldates = distinct([p.poll for p in practice_score])
        for poll in polldates:
            data = [round(p.score, 2) for p in practice_score if p.poll == poll]
            result.append({'name': str(poll)[:-24], "data": data})
        return result


class QuestionLineChart(PracticeScoreColumnChart):
    title = _(u'Question chart').format()
    chart_type = 'line'
    tooltip = {
        'shared': True,
        'crosshairs': True,
    }

    def get_data(self):
        data = super(QuestionLineChart, self).get_data()
        data['tooltip'] = self.tooltip
        data['yAxis']['min'] = 0.0
        return data

    @property
    def series(self):
        username = self.request.GET.get('username', None)
        if not username:
            return ''
        user = User.objects.filter(username=username).first()
        answers = Answer.objects.filter(respondent=user.respondent).order_by('question__question_text', 'poll__order')
        result = []
        polldates = distinct([answer.poll for answer in answers])
        self.categories = distinct([str(answer.question) for answer in answers])
        for poll in polldates:
            data = [round(answer.value, 2) for answer in answers if answer.poll == poll]
            result.append({'name': str(poll)[:-24], "data": data})
        return result


class PollDateBarChart(PracticeScoreColumnChart):
    title = _(u'Poll Date Practice Score').format()

    @property
    def series(self):
        poll_id = self.request.GET.get('poll_id', None)
        if not poll_id:
            return ''
        polldates = PollDate.objects.filter(poll=poll_id).order_by('order')
        self.categories = distinct([str(p.practice) for p in polldates[0].polldatepracticescore_set.all()])
        result = []
        for polldate in polldates:
            data = [round(p.score, 2) for p in polldate.polldatepracticescore_set.all()]
            result.append({'name': str(polldate)[:-24], "data": data})
        return result


class PollDateLineChart(QuestionLineChart):
    title = _(u'Poll Date Question Score').format()

    @property
    def series(self):
        poll_id = self.request.GET.get('poll_id', None)
        if not poll_id:
            return ''
        polldates = PollDate.objects.filter(poll=poll_id).order_by('order')
        self.categories = distinct([str(q.question) for q in
                                    polldates[0].polldatequestionscore_set.all().order_by('question__question_text')])
        result = []
        for polldate in polldates:
            data = [round(p.score, 2) for p in
                    polldate.polldatequestionscore_set.all().order_by('question__question_text')]
            result.append({'name': str(polldate)[:-24], "data": data})
        return result


class QuestionBarChart(PracticeScoreColumnChart):
    title = _(u'Question').format()
    yAxis = {
        'allowDecimals': True,
    }
    tooltip = {
        'crosshairs': True,
    }
    plotOptions = {
        'series': {
            'colorByPoint': True
        }
    }

    def get_data(self):
        data = super(QuestionBarChart, self).get_data()
        data['plotOptions'] = self.plotOptions
        return data

    @property
    def series(self):
        question_id = self.request.GET.get('question_id', None)
        if not question_id:
            return ''
        question = Question.objects.get(pk=question_id)
        if question.type == 'option':
            list_dict = list(Answer.objects.filter(question=question).order_by('option__order').values('option',
                                                                                                       'option__option_text').annotate(
                count=Count('option')))
            options = question.option_set.all().order_by('order').exclude(id__in=[d['option'] for d in list_dict])
            for option in options:
                d = {'count': 0, 'option': option.id, 'option__option_text': option.option_text}
                list_dict.append(d)
        else:
            list_dict = []
        self.categories = [d['option__option_text'] for d in list_dict]
        result = [{'name': [str(question)], "data": [dic['count'] for dic in list_dict]}]
        return result


class GBarView(View):
    def get(self, request, *args, **kwargs):
        get_object_or_404(Respondent, user=request.user)
        practice_scores = PracticeScore.objects.filter(respondent=request.user.respondent).order_by('practice__name',
                                                                                                    'poll__order')
        categories_p = distinct([str(p.poll)[:-24] for p in practice_scores])
        practices = distinct([practice_score.practice for practice_score in practice_scores])
        result_p = []
        for practice in practices:
            data = [round(p.score, 2) for p in practice_scores if p.practice == practice]
            result_p.append({'name': str(practice), "data": data})

        answers = Answer.objects.filter(respondent=request.user.respondent).order_by('question__question_text',
                                                                                     'poll__order')
        questions = distinct([answer.question for answer in answers])
        categories_q = distinct([str(answer.poll)[:-24] for answer in answers])
        result_q = []
        for question in questions:
            datas = [{'data': round(answer.value, 2), 'text': answer.text_value, 'answer': answer} for answer in answers
                     if answer.question == question]
            result_q.append({'name': str(question), "datas": datas})

        return render(request, "highcharts/graphic.html", {
            'result_p': result_p,
            'categories_p': categories_p,
            'categories_q': categories_q,
            'result_q': result_q,
            'username': request.user.username
        })


class ScoreView(View):
    def get(self, request, *args, **kwargs):
        get_object_or_404(Respondent, user=request.user)
        return render(request, "pages/questionnaire.html")
