from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from news_portal.models import Post


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=255, min_length=3)

    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'author']


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        try:
            basic_group = Group.objects.get(name='common')
        except Group.DoesNotExist:
            pass
        else:
            basic_group.user_set.add(user)
        return user
