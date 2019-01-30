# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from poll.models import Poll, Answer, RespondentPollDate, PracticeScore, PollDate, Respondent
from poll.forms import AnswerForm, DemographicsForm
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages


class QuestionnaireView(View):
    @classmethod
    def get_poll_available(cls, request, kwargs):
        user = request.user
        respondent_groups = user.groups.exclude(poll__isnull=True)
        if not user.has_perm('poll.is_respondent') or not respondent_groups.count():
            return None
        if kwargs.get('poll', None):
            polls = Poll.objects.filter(id=kwargs.get('poll'))
        else:
            polls = Poll.objects.filter(Group__in=respondent_groups)
        today = datetime.today().date()
        poll_dates = PollDate.objects.filter(poll__in=polls, start_date__lte=today, end_date__gte=today)
        poll_dates = poll_dates.exclude(respondentpolldate__completed=1)
        polls = Poll.objects.filter(polldate__in=poll_dates).distinct('id')
        return poll_dates, polls

    def get_poll_date(self, poll_dates, polls):
        poll, polldate = None, None
        if poll_dates and poll_dates.count() > 1 and polls.count() > 1:
            return 'list', 'list'
        if poll_dates and polls.count() == 1:
            polldate = poll_dates.first()
            poll = polldate.poll
        return polldate, poll

    def get(self, request, *args, **kwargs):
        get_object_or_404(Respondent, user=request.user)
        user = request.user
        poll_dates, polls = self.get_poll_available(self.request, self.kwargs)
        polldate, poll = self.get_poll_date(poll_dates, polls)
        if poll == 'list':
            return redirect(reverse_lazy('poll:poll_list'))
        message = _('There are no polls available for you.')
        if not polldate:
            return render(request, "pages/full-width.html", {'message': message, 'title': _('Excuse')})
        respondent_poll_date = user.respondent.respondentpolldate_set.filter(poll=polldate).first()
        if not respondent_poll_date:
            respondent_poll_date = RespondentPollDate(respondent=user.respondent, poll=polldate)

        if respondent_poll_date.completed == 1:
            return render(request, "pages/full-width.html", {'message': message, 'title': _('Excuse')})

        AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=0)

        for question in poll.questions.all():
            Answer.objects.get_or_create(respondent=user.respondent, question=question, practice=question.practice,
                                         poll=polldate, type=question.type)
        answers = Answer.objects.filter(respondent=user.respondent, poll=polldate)

        formset = AnswerFormSet(queryset=answers)
        return render(request, 'pages/questionnaire.html', {'formset': formset, 'polldate': polldate, 'poll': poll})

    def post(self, request, *args, **kwargs):
        get_object_or_404(Respondent, user=request.user)
        user = request.user
        poll_dates, polls = self.get_poll_available(self.request, self.kwargs)
        polldate, poll = self.get_poll_date(poll_dates, polls)
        respondent_poll_date, c = RespondentPollDate.objects.get_or_create(respondent=user.respondent, poll=polldate)
        AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=0)
        formset = AnswerFormSet(request.POST, request.FILES)
        if formset.is_valid():
            total_answer = Answer.objects.filter(respondent=user.respondent, poll=polldate).count()
            answers = formset.save()
            respondent_poll_date.completed = Answer.update_values(answers, total_answer)
            respondent_poll_date.save(update_fields=['completed'])
            PracticeScore.update_scores(user.respondent)
            message = _('Survey completed successfully, thank you very much for your time,')
            return render(request, "pages/full-width.html", {'message': message, 'title': _('Completed')})
        else:
            return render(request, "pages/questionnaire.html", {'formset': formset, 'polldate': polldate, 'poll': poll})


class UpdatePollDateScore(View):
    def get(self, request, *args, **kwargs):
        update_score_practice = request.GET.get('update_score_practice')
        update_score_question = request.GET.get('update_score_question')
        poll_id = request.GET.get('poll_id')
        poll = Poll.objects.get(pk=poll_id)
        for polldate in poll.polldate_set.all():
            if update_score_practice:
                polldate.update_practice_score()
            if update_score_question:
                polldate.update_question_score()
        return HttpResponse("<div id='ok'>ok</div>")


class PollListView(ListView):
    model = Poll

    def get_queryset(self):
        get_object_or_404(Respondent, user=self.request.user)
        poll_dates, polls = QuestionnaireView.get_poll_available(self.request, self.kwargs)
        self.queryset = polls
        return super(PollListView, self).get_queryset()


class DemographicsFormView(FormView):
    template_name = 'poll/forms/demographics_form.html'
    form_class = DemographicsForm
    success_url = '.'

    def get_initial(self):
        get_object_or_404(Respondent, user=self.request.user)
        initial = super(DemographicsFormView, self).get_initial()
        initial.update({'respondent': self.request.user.respondent})
        return initial

    def get_form_kwargs(self):
        kwargs = super(DemographicsFormView, self).get_form_kwargs()
        try:
            kwargs['instance'] = self.request.user.respondent.demographics
        except Exception as e:
            print e.message
        return kwargs

    def form_valid(self, form):
        if form.save():
            messages.success(self.request, _(u'Your demographic information was saved successfully'))
        return super(DemographicsFormView, self).form_valid(form)
