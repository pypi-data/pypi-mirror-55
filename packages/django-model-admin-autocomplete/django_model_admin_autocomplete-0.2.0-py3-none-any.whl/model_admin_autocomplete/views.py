import operator
from functools import reduce

from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.http import JsonResponse
from django.db import models


class ModelAdminAutocompleteJsonView(AutocompleteJsonView):
    autocomplete_model = None
    search_fields = ()

    def clean_search_fields(self):
        return ['__'.join(field.split("__")[1:]) for field in self.search_fields]

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """

        if not self.has_perm(request):
            return JsonResponse({'error': '403 Forbidden'}, status=403)

        self.term = request.GET.get('term', '')
        self.paginator_class = self.model_admin.paginator
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {'id': str(obj.pk), 'text': f"{str(obj)}"}
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })

    def get_queryset(self):
        if self.term:
            or_queries = [models.Q(**{'%s__icontains' % search_field: self.term}) for search_field in self.clean_search_fields()]
            queryset = self.autocomplete_model.objects.filter(reduce(operator.or_, or_queries))
            return queryset
        else:
            return self.autocomplete_model.objects.all()
