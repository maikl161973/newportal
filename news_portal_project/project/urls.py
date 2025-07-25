"""news_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include

from news_portal import views
from news_portal.views import (NewsList, NewsDetail, NewsListSearch, NewsCreate, \
    NewsUpdate, NewsDelete, ArticleCreate, ArticleDelete, ArticleUpdate, \
    BaseRegisterView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base),
    path('user_update', views.user_update, name='set_author_user'),
    # path('login/', LoginView.as_view(template_name='login.html'),
    #      name='login'),
    # path('logout/', LogoutView.as_view(template_name='logout.html'),
    #      name='logout'),
    # path('signup/', BaseRegisterView.as_view(template_name='signup.html'),
    #      name='signup'),
    # path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/search/', NewsListSearch.as_view(), name='news_list_with_search'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view()),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view()),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view()),

]
