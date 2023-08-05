from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet, DateFilter
from django_filters import BooleanFilter

from irekua_database.models import SamplingEventDevice



class Filter(FilterSet):
    is_own = BooleanFilter(
        method='user_owns_object',
        label=_('Mine'),
        widget=forms.CheckboxInput())

    class Meta:
        model = SamplingEventDevice
        fields = {
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'collection_device__physical_device__device__brand__name': ['icontains'],
            'collection_device__physical_device__device__model': ['icontains'],
            'collection_device__physical_device__device__device_type': ['exact'],
            'created_on': ['gt', 'lt'],
        }

    def user_owns_object(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(collection_device__created_by=user)
        return queryset

search_fields = (
    'collection_device__physical_device__device__serial_number',
    'collection_device__physical_device__device__brand__name',
    'collection_device__physical_device__device__model'
)


ordering_fields = (
    ('created_on', _('added on')),
)
