from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from news_portal.models import Post, NEWS


def base(request):
    return render(request, 'default.html')


class NewsList(ListView):
    model = Post
    orderig = '-created'
    template_name = 'news.html'
    context_object_name = 'news'
    fields = ['title', 'created', 'contents']

    def get_queryset(self):
        return self.model.objects.filter(post_type=NEWS).order_by(self.orderig)


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
