# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from poll.forms import RespondentForm, OptionInlineForm, PollForm
from suit.admin import SortableTabularInline

from poll.models import Question, Poll, Demographics, Respondent, Option, Practice, Answer, PollDate, \
    RespondentPollDate, PracticeScore

from poll.actions import export_report_respondent_as_csv


# Register your models here.
class PollDateInline(SortableTabularInline):
    model = PollDate
    extra = 0
    min_num = 2
    sortable = 'order'
    suit_classes = 'suit-tab suit-tab-polldates'


class OptionInline(SortableTabularInline):
    form = OptionInlineForm
    model = Option
    extra = 0
    min_num = 2
    sortable = 'order'
    readonly_fields = ('number',)
    suit_classes = 'suit-tab suit-tab-general'

    def number(self, obj):
        return obj.order + 1


class RespondentPollDateInline(SortableTabularInline):
    model = RespondentPollDate
    extra = 0
    max_num = 0
    sortable = 'id'
    readonly_fields = ('poll', 'poll_score', 'date')
    can_delete = False
    suit_classes = 'suit-tab suit-tab-general'


class PracticeScoreInline(SortableTabularInline):
    model = PracticeScore
    extra = 0
    max_num = 0
    sortable = 'id'
    readonly_fields = ('practice', 'score', 'poll')
    can_delete = False
    suit_classes = 'suit-tab suit-tab-general'


class AnswerInline(SortableTabularInline):
    model = Answer
    extra = 0
    max_num = 0
    sortable = 'id'
    readonly_fields = ('polldate', 'question', 'answer', '_value',)
    exclude = ('text_value', 'practice', 'resolved', 'poll', 'options', 'option', 'type', 'value')
    can_delete = False
    suit_classes = 'suit-tab suit-tab-answer'

    def polldate(self, obj):
        return str(obj.poll)[:-24]

    def _value(self, obj):
        return "{0:.2f}".format(obj.value, 2)

    _value.short_description = _('value')


class PollAdmin(admin.ModelAdmin):
    form = PollForm
    readonly_fields = ('create_date', 'last_modified',)
    inlines = [PollDateInline]
    filter_horizontal = ('questions',)
    list_display = ('title', 'description', 'Group', 'create_date', 'last_modified')
    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [('title', 'Group'), 'description', 'questions', ('create_date', 'last_modified')]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-polldates',),
            'description': 'Tabs can contain any fieldsets and inlines',
            'fields': []}),
    ]

    suit_form_tabs = (('general', _('General')),
                      ('polldates', _('Poll dates')),
                      ('statistics_graphs', _('Statistics and graphs')),)
    suit_form_includes = (
        ('admin/poll/poll/tag/statistics_graphs.html', '', 'statistics_graphs'),
    )

    class Media:
        css = {
            'all': ('css/bootstrap-datepicker3.min.css',)
        }
        js = ('js/highcharts/jquery-migrate-1.2.1.min.js', 'js/jquery.dataTables.min.js',
              'django_datatable_view_extension/js/datatable_extension.js', 'js/highcharts/highcharts.js',
              'js/bootstrap-datepicker/bootstrap-datetimepicker.min.js',
              'js/bootstrap-datepicker/locale/bootstrap-datepicker.es.js',
              'js/highcharts/exporting.js', 'js/poll/tools.js', 'js/poll/app.admin.js',)


class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('original_question_text', 'practice', 'type')
    list_filter = ('create_date', 'practice')
    readonly_fields = ('order', 'create_date', 'last_modified',)
    search_fields = ('original_question_text',)
    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [('order', 'create_date', 'last_modified',), 'practice', 'original_question_text',
                       'question_text', 'type']
        })
    ]

    suit_form_tabs = (
        ('general', _('General')),
        ('statistics-graphs-question', _('Statistics and graphs')),
    )
    suit_form_includes = (
        ('admin/poll/question/tag/statistics_graphs.html', '', 'statistics-graphs-question'),
    )

    class Media:
        js = ('js/highcharts/jquery-migrate-1.2.1.min.js', 'js/jquery.dataTables.min.js',
              'django_datatable_view_extension/js/datatable_extension.js', 'js/highcharts/highcharts.js',
              'js/highcharts/exporting.js', 'js/poll/tools.js', 'js/poll/app.admin.js')


class QuestionInline(SortableTabularInline):
    model = Question
    extra = 0
    max_num = 0
    exclude = ('question_text',)
    readonly_fields = ('original_question_text',)
    sortable = 'order'


class DemographicsInline(admin.StackedInline):
    model = Demographics
    suit_classes = 'suit-tab suit-tab-general'


class RespondentAdmin(admin.ModelAdmin):
    inlines = (DemographicsInline, RespondentPollDateInline, PracticeScoreInline, AnswerInline)
    form = RespondentForm
    actions = [export_report_respondent_as_csv]
    list_display = ('identification_number', '__str__',)
    search_fields = ['identification_number', 'user__username', 'user__first_name', 'user__last_name']
    list_filter = ('user__groups',)
    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['identification_number', 'first_name', 'last_name', 'username', 'group'],
        })
    ]
    suit_form_tabs = (
        ('general', _('General')),
        ('answer', _('Answers')),
        # ('answer_by_user', _('Answers')),
        ('statistics_graphs', _('Statistics and graphs')),
    )
    suit_form_includes = (
        ('admin/poll/respondent/tag/statistics_graphs.html', '', 'statistics_graphs'),
        # ('poll/admin/datatable.html', '', 'answer_by_user'),
    )

    class Media:
        css = {
            'all': ('css/bootstrap-datepicker3.min.css',)
        }
        js = ('js/highcharts/jquery-migrate-1.2.1.min.js', 'js/jquery.dataTables.min.js',
              'django_datatable_view_extension/js/datatable_extension.js', 'js/highcharts/highcharts.js',
              'js/bootstrap-datepicker/bootstrap-datetimepicker.min.js',
              'js/bootstrap-datepicker/locale/bootstrap-datepicker.es.js',
              'js/highcharts/exporting.js', 'js/poll/tools.js', 'js/poll/app.admin.js',)

    def save_model(self, request, obj, form, change):
        form.save()

    def delete_model(self, request, obj):
        obj.user.delete()

    def get_actions(self, request):
        actions = super(RespondentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class PracticeAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'option', 'practice', 'poll', 'respondent', 'resolved')
    list_filter = ('poll', 'practice')
    filter_horizontal = ('options',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Practice, PracticeAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Respondent, RespondentAdmin)
admin.site.register(Answer, AnswerAdmin)
