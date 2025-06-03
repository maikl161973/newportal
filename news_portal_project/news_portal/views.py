import datetime

from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)

from news_portal.filters import NewsFilter
from news_portal.forms import NewsForm
from news_portal.models import Post, NEWS, ARTICLE


def base(request):
    return render(request, 'default.html')


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


class BaseCreate(CreateView):
    post_type = None
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.created = datetime.datetime.today()
        news.post_type = self.post_type
        return super().form_valid(form)


class BaseUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class BaseDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class NewsCreate(BaseCreate):
    post_type = NEWS


class NewsUpdate(BaseUpdate):
    """Изменение новости"""


class NewsDelete(BaseDelete):
    """Удаление новости"""


class ArticleCreate(NewsCreate):
    post_type = ARTICLE


class ArticleUpdate(BaseUpdate):
    """Изменение статьи"""


class ArticleDelete(BaseDelete):
    """Добавление статьи"""

