from django.shortcuts import get_object_or_404

class DetailMultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        multi_filter = {self.lookup_query_fields[field]: self.kwargs[field] for field in self.lookup_fields}
        obj = get_object_or_404(queryset, **multi_filter)
        self.check_object_permissions(self.request, obj)
        return obj