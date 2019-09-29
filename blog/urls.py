"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from blog.views import home_page, blog_post, home_page_redirect, create_comment, login_view, logout_view, edit_blog_post, new_article, health_view, growth_view, management_view, spirituality_view, novels_view, anecdotes_view, search
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_page, name='home'),
    path('', home_page_redirect),
    path('post/<int:id>', blog_post, name='blog_post'),
    path('post/<int:id>/edit', edit_blog_post, name='edit_blog_post'),
    path('post/comment/', create_comment, name='create_comment'),
    path('create/', new_article, name='new_article_page'),
    path('create/', new_article, name='create_article'),
    path('accounts/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('Health/', health_view, name='health_view'),
    path('Growth/', growth_view, name='growth_view'),
    path('Management/', management_view, name='management_view'),
    path('Spirituality/', spirituality_view, name='spirituality_view'),
    path('Novels/', novels_view, name='novels_view'),
    path('Anecdotes/', anecdotes_view, name='anecdotes_view'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^search/$', search, name='search'),
]
