# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from poll.models import Answer, Option, Respondent, Poll, Demographics
from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext_lazy as _


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance:
            queryset = Option.objects.filter(question=self.instance.question)
            if instance.question.type == 'option':
                self.fields['option'].queryset = queryset
                self.fields['option'].required = True
                self.fields['options'].required = False
            elif instance.question.type == 'options':
                self.fields['options'].queryset = queryset
                self.fields['option'].required = False
                self.fields['options'].required = True

    class Meta:
        model = Answer
        fields = '__all__'
        exclude = ('type', 'value',)
        widgets = {'respondent': forms.HiddenInput(), 'poll': forms.HiddenInput(), 'practice': forms.HiddenInput(),
                   'question': forms.HiddenInput(), 'options': forms.CheckboxSelectMultiple()}


class RespondentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, label=_('first name'))
    last_name = forms.CharField(max_length=40, label=_('last name'))
    username = forms.CharField(max_length=20, label=_('username'))
    group = forms.ModelChoiceField(
        label=_('Group'),
        queryset=Group.objects.exclude(poll__isnull=True),
        empty_label=""
    )

    def __init__(self, *args, **kwargs):
        super(RespondentForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['username'].initial = self.instance.user.username
            self.fields['group'].initial = self.instance.user.groups.exclude(poll__isnull=True).first()

    @classmethod
    def add_perm_respondent(cls, user):
        content_type = ContentType.objects.get_for_model(Respondent)
        is_respondent = Permission.objects.get(content_type=content_type, codename='is_respondent')
        user.user_permissions.add(is_respondent.id)

    def save(self, commit=True):
        respondent = super(RespondentForm, self).save(commit=False)
        if not getattr(respondent, 'user', None):
            user = User()
            user.set_password(self.cleaned_data['identification_number'])
        else:
            user = respondent.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            user.groups.add(self.cleaned_data['group'])
            respondent.user = user
            respondent.save()
            self.add_perm_respondent(user)
        return respondent

    class Meta:
        model = Respondent
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}


class OptionInlineForm(forms.ModelForm):
    class Meta:
        widgets = {
            'option_text': forms.TextInput(attrs={'class': 'input-xlarge'}),
        }


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'

    def clean(self):
        return super(PollForm, self).clean()


class DemographicsForm(forms.ModelForm):
    class Meta:
        model = Demographics
        fields = '__all__'
        widgets = {'respondent': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(DemographicsForm, self).__init__(*args, **kwargs)
        self.fields['date_birth'].widget.attrs.update({
            'class': 'form-control datepicker',
        })
