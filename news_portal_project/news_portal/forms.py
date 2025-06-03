from django import forms

from news_portal.models import Post


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=255, min_length=3)

    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'author']

