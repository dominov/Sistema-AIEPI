from django_datatable_view_extension.base_datatable_view import DataTableView

from poll.models import Answer


class AnswersByUserJsonView(DataTableView):
    model = Answer
    columns = ['id']
    order_columns = columns[:]
    max_display_length = 100

    def get_initial_queryset(self):
        query_set = super(AnswersByUserJsonView, self).get_initial_queryset()
        return query_set
