__author__ = 'leon'
from django.http import HttpResponse
from django.utils.translation import ugettext as _
import csv
from django.utils.encoding import smart_str

from poll.models import Answer

EXPORT = {
    'name': 0,
}


def export_report_respondent_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    opts = modeladmin.model._meta
    field_names = [smart_str(field.name) for field in opts.fields]
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([smart_str(getattr(obj, field)) for field in field_names])
    return response


export_report_respondent_as_csv.short_description = _(u"Export CSV")
