# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from django.core.validators import MinValueValidator


class SIIMCIConfig(SingletonModel):
    site_name = models.CharField(_("site name"), max_length=255, default=_('SI-IMCI'))
    # respondents_group = models.ForeignKey(Group, null=True, verbose_name=_('respondents group'))
    poll_repetitions = models.IntegerField(_('poll repetitions'), default=2, validators=[MinValueValidator(1)])
    logo = models.ImageField(_('logo'), null=True, blank=True,
                             help_text=_('if this field is fill will replace the site name'))
    create_date = models.DateField(_('create date'), auto_now_add=True, null=True)
    last_modified = models.DateField(_('last-modified'), auto_now=True, null=True)
    copyright = models.CharField(_('copyright'), max_length=255, default='SI-IMCI')

    class Meta:
        verbose_name = _("SI-IMCI Configuration")
        verbose_name_plural = _("SI-IMCI Configuration")

    def image_tag(self):
        return u'<img src="%s" />' % self.logo
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
