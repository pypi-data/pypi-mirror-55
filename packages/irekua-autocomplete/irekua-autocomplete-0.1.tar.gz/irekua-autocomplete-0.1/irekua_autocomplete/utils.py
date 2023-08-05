from django.urls import reverse
from dal import autocomplete


def get_autocomplete_widget(model):
    name = model._meta.verbose_name_plural.lower().replace(' ', '_')
    view_name = '{name}_autocomplete'.format(name=name)
    url = reverse(view_name)
    return autocomplete.ModelSelect2(url=url)
