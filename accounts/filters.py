import django_filters
from .models import Order
from django_filters import CharFilter

class OrderFilter(django_filters.FilterSet):
    note = CharFilter(field_name = 'note',lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_created','tags']