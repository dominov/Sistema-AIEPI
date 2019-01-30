# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.db import IntegrityError
from django.db import transaction
from django.db.models import Avg
from django.contrib.auth.models import Group, User
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _

from poll.templatetags.poll_tag import distinct
from poll.chioces import FIELD, EDUCATION, GENDER


# Create your models here.


class Practice(models.Model):
    name = models.CharField(_('name'), max_length=200)
    short_name = models.CharField(_('short name'), max_length=10, null=True)
    description = models.TextField(_('description'))
    create_date = models.DateField(_('create date'), auto_now_add=True, null=True)
    last_modified = models.DateField(_('last-modified'), auto_now=True, null=True)

    @staticmethod
    def get_score_practice():
        pass

    class Meta:
        verbose_name = _('practice')
        verbose_name_plural = _('practices')

    def __str__(self):
        return self.name


class Question(models.Model):
    practice = models.ForeignKey(Practice, null=True, verbose_name=_('practice'))
    original_question_text = models.TextField(_('original question text'))
    question_text = models.TextField(_('question text'))
    order = models.PositiveIntegerField(_('order'), default=0)
    type = models.CharField(_('type'), max_length=10, choices=FIELD, default=FIELD.OPTION)
    create_date = models.DateField(_('create date'), auto_now_add=True, null=True)
    last_modified = models.DateField(_('last-modified'), auto_now=True, null=True)

    class Meta:
        ordering = ['question_text']
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.original_question_text


class Poll(models.Model):
    title = models.CharField(_('title'), max_length=200)
    Group = models.ForeignKey(Group, verbose_name=_('group'))
    description = models.TextField(_('description'), null=True)
    create_date = models.DateField(_('create date'), auto_now_add=True, null=True)
    last_modified = models.DateField(_('last-modified'), auto_now=True, null=True)
    questions = models.ManyToManyField(Question, verbose_name=_('questions'))

    class Meta:
        verbose_name = _('poll')
        verbose_name_plural = _('polls')

    def get_available(self):
        today = datetime.now().date()
        return self.polldate_set.filter(start_date__lte=today, end_date__gte=today).exclude(
            respondentpolldate__completed=1).first()

    def save(self, *args, **kwargs):
        if self.id:
            poll = Poll.objects.get(pk=self.id)
        else:
            poll = self
        super(Poll, self).save(*args, **kwargs)
        if self.questions != poll.questions:
            for polldate in self.polldate_set.all():
                polldate.create_practice_score()
                polldate.create_question_score()

    def __str__(self):
        return self.title


class Option(models.Model):
    question = models.ForeignKey(Question, verbose_name=_('question'))
    option_text = models.CharField(_('option text'), max_length=200, blank=True)
    value = models.FloatField(_('value'), default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    order = models.PositiveIntegerField(_('order'), default=0)
    create_date = models.DateField(_('create date'), auto_now_add=True, null=True)
    last_modified = models.DateField(_('last-modified'), auto_now=True, null=True)

    class Meta:
        ordering = ['option_text']
        verbose_name = _('option')
        verbose_name_plural = _('options')

    def __str__(self):
        return self.option_text


class Respondent(models.Model):
    identification_number = models.IntegerField(_('identification number'), unique=True, null=True, db_index=True)
    user = models.OneToOneField(User, verbose_name=_('user'), blank=True)

    class Meta:
        verbose_name = _('respondent')
        verbose_name_plural = _('respondents')

        permissions = (
            ("is_respondent", _(u"Is respondent")),
        )

    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)


class Demographics(models.Model):
    respondent = models.OneToOneField(Respondent, null=True, verbose_name=_('respondent'))
    date_birth = models.DateField(_('date birth'))
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER, default=GENDER.FEMALE)
    health_insurance = models.BooleanField(_('health insurance'), default=False)
    EPS = models.CharField(_('EPS'), max_length=200, null=True, blank=True)
    country = CountryField(_('country'), default='CO')
    neighborhood = models.CharField(_('neighborhood'), max_length=200)
    city = models.CharField(_('city'), max_length=200)
    child_vaccination_card = models.BooleanField(_('child vaccination card'), default=False)
    child_name = models.CharField(_('child name'), max_length=200)
    education_level = models.CharField(_('education level'), max_length=1, choices=EDUCATION, default=EDUCATION.PRIMARY)
    create_date = models.DateField(_('create date'), auto_now_add=True, null=True)
    last_modified = models.DateField(_('last-modified'), auto_now=True, null=True)

    class Meta:
        verbose_name = _('demographics')
        verbose_name_plural = _('demographics')

    def __str__(self):
        return self.education_level


class PollDate(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_('poll'))
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('poll date')
        verbose_name_plural = _('poll dates')

    def save(self, *args, **kwargs):
        super(PollDate, self).save(*args, **kwargs)
        self.create_practice_score()
        self.create_question_score()

    def create_practice_score(self):
        for practice in distinct([question.practice for question in self.poll.questions.all()]):
            try:
                with transaction.atomic():
                    self.polldatepracticescore_set.create(practice=practice)
            except IntegrityError as e:
                print e

    def create_question_score(self):
        for question in self.poll.questions.all():
            try:
                with transaction.atomic():
                    self.polldatequestionscore_set.create(question=question)
            except IntegrityError as e:
                print str(e)

    def update_practice_score(self):
        for item in self.polldatepracticescore_set.all():
            item.update_score()

    def update_question_score(self):
        for item in self.polldatequestionscore_set.all():
            item.update_score()

    def __str__(self):
        return str(self.poll) + ' #' + str(self.order + 1) + ' [' + str(self.start_date) + "-" + str(
            self.end_date) + ']'


class Answer(models.Model):
    practice = models.ForeignKey(Practice, null=True, verbose_name=_('practice'))
    poll = models.ForeignKey(PollDate, null=True, verbose_name=_('poll'))
    question = models.ForeignKey(Question, verbose_name=_('question'))
    option = models.ForeignKey(Option, null=True, verbose_name=_('option'))
    options = models.ManyToManyField(Option, verbose_name=_('options'), related_name='options')
    respondent = models.ForeignKey(Respondent, verbose_name=_('respondent'))
    type = models.CharField(_('type'), max_length=10, choices=FIELD, default=FIELD.OPTION)
    value = models.FloatField(_('value'), default=0.0, )
    text_value = models.CharField(_('Text value'), max_length=255, blank=True, null=True)
    resolved = models.BooleanField(_('resolved'), default=False)
    create_date = models.DateField(_('create date'), auto_now_add=True, null=True)
    last_modified = models.DateField(_('last-modified'), auto_now=True, null=True)

    @staticmethod
    def update_values(answers, total_answer):
        number_of_answers = total_answer
        number_of_answers_saved = 0
        for answer in answers:
            value, resolved = answer.update_value(commit=True)
            if resolved:
                number_of_answers_saved += 1
        try:
            return float(number_of_answers_saved) / float(number_of_answers)
        except:
            return 0.0

    def get_options_value(self):
        options = self.options.all()
        if options:
            return sum([option.value for option in options]) / len(options)
        else:
            return 0.0

    def update_value(self, commit=False):
        self.resolved, self.text_value = False, None
        self.type = self.question.type
        if self.type == 'option':
            self.value = self.option.value
            self.text_value = u'{}'.format(self.option)
        elif self.type == 'options':
            self.value = self.get_options_value()
            options = [option.order + 1 for option in self.options.all().order_by('order')]
            self.text_value = u'{}'.format(options if options else '')
        if self.text_value:
            self.resolved = True
        if commit:
            self.save()
        return self.value, self.resolved

    def answer(self):
        if self.type == 'option':
            return self.option
        elif self.type == 'options':
            return [option.order + 1 for option in self.options.all().order_by('order')]

    answer.short_description = _('answer')

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')


class RespondentPollDate(models.Model):
    poll = models.ForeignKey(PollDate, verbose_name=_('poll'))
    respondent = models.ForeignKey(Respondent, verbose_name=_('respondent'))
    date = models.DateTimeField(_('date'), auto_now_add=True)
    completed = models.FloatField(_('completed'), default=0.0,
                                  validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    poll_score = models.FloatField(_('poll score'), default=0.0)

    class Meta:
        ordering = ['date']
        verbose_name = _('poll date')
        verbose_name_plural = _('poll dates')


class PracticeScore(models.Model):
    poll = models.ForeignKey(PollDate, verbose_name=_('poll'))
    respondent = models.ForeignKey(Respondent, verbose_name=_('respondent'))
    practice = models.ForeignKey(Practice, verbose_name=_('practice'))
    score = models.FloatField(_('score'))

    @staticmethod
    def get_score(answers=[]):
        if not answers:
            return 0.0
        return sum([answer.value for answer in answers]) / len(answers)

    @staticmethod
    def update_scores(respondent):
        respondentpolldates = respondent.respondentpolldate_set.all()
        answers = Answer.objects.filter(respondent=respondent).distinct('practice')
        practices = [answer.practice for answer in Answer.objects.filter(respondent=respondent).distinct('practice')]
        for respondentpoll in respondentpolldates:
            poll_score = 0.0
            for practice in practices:
                score = PracticeScore.get_score(
                    Answer.objects.filter(practice=practice, respondent=respondent, poll=respondentpoll.poll))
                poll_score += score
                practice_score = PracticeScore.objects.filter(respondent=respondent, practice=practice,
                                                              poll=respondentpoll.poll).first()
                if practice_score:
                    practice_score.score = score
                else:
                    practice_score = PracticeScore(score=score, respondent=respondent, practice=practice,
                                                   poll=respondentpoll.poll)
                practice_score.save()
            respondentpoll.poll_score = poll_score / len(practices)
            respondentpoll.save()

    class Meta:
        verbose_name = _('practice score')
        verbose_name_plural = _('practice scores')


class PollDatePracticeScore(models.Model):
    practice = models.ForeignKey(Practice, verbose_name=_('practice'))
    poll_date = models.ForeignKey(PollDate, verbose_name=_('poll date'))
    score = models.FloatField(_('average score'), default=0.0)
    last_modified = models.DateField(_('last-modified'), auto_now=True, null=True)

    class Meta:
        unique_together = ('practice', 'poll_date')

    def update_score(self):
        dic = PracticeScore.objects.filter(poll=self.poll_date, practice=self.practice).aggregate(average=Avg('score'))
        self.score = dic['average']
        self.save()


class PollDateQuestionScore(models.Model):
    question = models.ForeignKey(Question, verbose_name=_('question'))
    poll_date = models.ForeignKey(PollDate, verbose_name=_('poll date'))
    score = models.FloatField(_('average score'), default=0.0)
    last_modified = models.DateField(_('last-modified'), auto_now=True, null=True)

    class Meta:
        unique_together = ('question', 'poll_date')

    def update_score(self):
        dic = Answer.objects.filter(poll=self.poll_date, question=self.question).aggregate(average=Avg('value'))
        self.score = dic['average']
        self.save()
