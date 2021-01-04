# Case insensitive Mixin for unique=Treu Data Fiels
# https://concisecoder.io/2018/10/27/case-insensitive-fields-in-django-models/

class CaseInsensitiveFieldMixin:
    
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }
    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)