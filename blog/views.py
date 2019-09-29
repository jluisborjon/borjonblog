# import ipdb
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blog.models import Article, CommentForm, ArticleForm
from blog.forms import LoginForm
import datetime
from ckeditor.fields import RichTextField
from .filters import ArticleFilter


""" Defined home_page (request & HttpResponse) """
def home_page(request):
    now = str(datetime.datetime.now())
    articles = Article.objects.filter(draft=False).order_by('-published_date')[:1]
    context = {'name': 'Borjon', 'day': now, 'articles': articles}
    response = render(request, 'index1.html', context)
    return HttpResponse(response)

def search(request):
    article_list = Article.objects.all()
    article_filter = ArticleFilter(request.GET, queryset=article_list)
    return render(request, 'search/article_list.html', {'filter': article_filter})


""" Defined health_view (request & HttpResponse) """
def health_view(request):
    now = str(datetime.datetime.now())
    articles = Article.objects.filter(category = 'Para la Salud', draft=False).order_by('-published_date').all()
    context = {'name': 'Borjon', 'day': now, 'articles': articles}
    response = render(request, 'index.html', context)
    return HttpResponse(response)



""" Defined growth_view (request & HttpResponse) """
def growth_view(request):
    now = str(datetime.datetime.now())
    articles = Article.objects.filter(category = 'Superación Personal', draft=False).order_by('-published_date').all()
    context = {'name': 'Borjon', 'day': now, 'articles': articles}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

""" Defined management_view (request & HttpResponse) """
def management_view(request):
    now = str(datetime.datetime.now())
    articles = Article.objects.filter(category = 'Administración', draft=False).order_by('-published_date').all()
    context = {'name': 'Borjon', 'day': now, 'articles': articles}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

""" Defined spirituality_view (request & HttpResponse) """
def spirituality_view(request):
    now = str(datetime.datetime.now())
    articles = Article.objects.filter(category = 'Espiritualidad', draft=False).order_by('-published_date').all()
    context = {'name': 'Borjon', 'day': now, 'articles': articles}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

""" Defined novels_view (request & HttpResponse) """
def novels_view(request):
    now = str(datetime.datetime.now())
    articles = Article.objects.filter(category = 'Novelas', draft=False).order_by('-published_date').all()
    context = {'name': 'Borjon', 'day': now, 'articles': articles}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

""" Defined anecdotes_view (request & HttpResponse) """
def anecdotes_view(request):
    now = str(datetime.datetime.now())
    articles = Article.objects.filter(category = 'Anécdotas de mi Tierra', draft=False).order_by('-published_date').all()
    context = {'name': 'Borjon', 'day': now, 'articles': articles}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

""" Defined home_page_redirect """
def home_page_redirect(request):
    return redirect(home_page)

""" Defined blog_post """
def blog_post(request, id):
    post = get_object_or_404(Article, pk=id)
    if post.comments.count() > 0:
        comment_count = True
    else:
        comment_count = False
    new_form = CommentForm(initial={'article': id})
    context = {'article': post, 'comments': comment_count, 'form': new_form}
    html = render(request, 'post.html', context)
    return HttpResponse(html)

""" Defined login validation to create an article (only for admin now). """
@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.user = request.user
            new_article = form.save()
            return HttpResponseRedirect('/post/' + str(new_article.id))
    else:
        form = ArticleForm()
    response = render(request, 'create.html', {'form': form})
    return HttpResponse(response)

""" Defined login validation to create a new article (only for admin now). """
@login_required
def new_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save()
            new_article.user = request.user
            new_article.save()
            return HttpResponseRedirect('/post/{}'.format(new_article.id))
    else:
        form = ArticleForm()
    response = render(request, 'create.html', {'form': form})
    return HttpResponse(response)

""" Defined create_comment """
""" for now anyone can add a comment """
""" If users' get created we can add login validation to add a comment """
def create_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save()
        return HttpResponseRedirect('/post/' + request.POST['article'])
    else:
        print(form.errors)
        response = render(request, 'index.html')
        return HttpResponse(response)

""" Defined login_view (only for admin now). If needed we can add users) """
""" And users' validation view"""
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()
    context = {'form': form}
    response = render(request, 'login.html', context)
    return HttpResponse(response)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')

""" Defined edit_post validation (only for admin now). """
def edit_blog_post(request, id):
    article = get_object_or_404(Article, pk=id, user=request.user)
    if request.method == 'GET':
        form = ArticleForm(instance=article)
        context = {'form': form, 'article': article}
        response = render(request, 'edit_post.html', context)
        return HttpResponse(response)
    elif request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            updated_article = form.save()
            return HttpResponseRedirect('/post/{}'.format(article.id))
        else:
            context = {'form': form, 'article': article}
            response = render(request, 'edit_post.html', context)
            return HttpResponse(response)
