from django import forms
from django_filters import FilterSet, DateFilter

from news_portal.models import Post


class NewsFilter(FilterSet):
    created = DateFilter(
        field_name='created',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
            lookup_expr='gt', label='Created post'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user__username': ['exact'],
            # 'created': ['gt']
        }