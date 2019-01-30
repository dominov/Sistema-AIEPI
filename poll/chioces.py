from django.utils.translation import ugettext_lazy as _
from django_choices_flow import Choices


class FIELD(Choices):
    OPTION = 'option', _('Selection')
    OPTIONS = 'options', _('Multi Selection')


class GENDER(Choices):
    FEMALE = 'F', _('Female')
    MALE = 'M', _('Male')


class EDUCATION(Choices):
    PRIMARY = '1', _('Primary')
    SECONDARY = '2', _('Secondary')
    TECHNICAL = '3', _('technical')
    TECHNOLOGIST = '4', _('Technologist')
