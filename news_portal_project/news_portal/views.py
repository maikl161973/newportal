import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)

from news_portal.filters import NewsFilter
from news_portal.forms import NewsForm, BaseRegisterForm
from news_portal.models import Post, NEWS, ARTICLE


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


def base(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'Гость'

    return render(
        request, 'main.html', context={
            'is_user_not_auth': not request.user.is_authenticated,
            'username': username
        })


@login_required
def user_update(request):
    authors = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors.user_set.add(request.user)
    return redirect('/')


class NewsList(ListView):
    model = Post
    orderig = '-created'
    template_name = 'news.html'
    context_object_name = 'news'
    fields = ['title', 'created', 'contents']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post_type=NEWS).order_by(self.orderig)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.user.is_authenticated:
            context['is_author'] = (
                self.request.user.groups.filter(name='authors').exists())
        else:
            context['is_author'] = False

        return context


class NewsListSearch(NewsList):

    template_name = 'search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'detail_news.html'
    context_object_name = 'detail_news'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return HttpResponseNotFound(
                '<p align="center" style="font-size: 20px; color:red"'
                '>Не найдена новость с идентификатором "{}"<p>'.format(
                    kwargs['pk']
                )
            )
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class BaseCreate(PermissionRequiredMixin, CreateView):
    post_type = None
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news_portal.add_post',)

    def form_valid(self, form):
        news = form.save(commit=False)
        news.created = datetime.datetime.today()
        news.post_type = self.post_type
        return super().form_valid(form)


@method_decorator(login_required, name='get')
class BaseUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news_portal.change_post',)


class BaseDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news_portal.delete_post',)


class NewsCreate(BaseCreate):
    post_type = NEWS


@method_decorator(login_required, name='get')
class NewsUpdate(BaseUpdate):
    """Изменение новости"""


class NewsDelete(BaseDelete):
    """Удаление новости"""


class ArticleCreate(NewsCreate):
    post_type = ARTICLE


# @method_decorator(login_required)
class ArticleUpdate(BaseUpdate):
    """Изменение статьи"""


class ArticleDelete(BaseDelete):
    """Добавление статьи"""
