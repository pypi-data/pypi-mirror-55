from django.urls import path

from . import views
from .term_autocomplete import TermListView


urlpatterns = [
    path(
        'institutions/',
        views.InstitutionAutocomplete.as_view(),
        name='institutions_autocomplete'),
    path(
        'device_brands/',
        views.DeviceBrandAutocomplete.as_view(create_field="name"),
        name='device_brands_autocomplete'),
    path(
        'devices/',
        views.DeviceAutocomplete.as_view(),
        name='devices_autocomplete'),
    path(
        'collections/',
        views.CollectionAutocomplete.as_view(),
        name='collection_autocomplete'),
    path(
        'collection_types/',
        views.CollectionTypeAutocomplete.as_view(),
        name='collection_type_autocomplete'),
    path(
        'metacollections/',
        views.MetacollectionAutocomplete.as_view(),
        name='metacollection_autocomplete'),
    path(
        'terms/',
        views.TermsAutocomplete.as_view(),
        name='terms_autocomplete'),
    path(
        'tags/',
        views.TagsAutocomplete.as_view(),
        name='tags_autocomplete'),
    path(
        'annotation_tools/',
        views.AnnotationToolsAutocomplete.as_view(),
        name='annotation_tools_autocomplete'),
    path(
        'sampling_event_types/',
        views.SamplingEventTypesAutocomplete.as_view(),
        name='sampling_event_types_autocomplete'),
    path(
        'users/',
        views.UserAutocomplete.as_view(),
        name='users_autocomplete'),
    path(
        'event_type/<pk>/terms/',
        TermListView.as_view(),
        name='term_autocomplete')
]
