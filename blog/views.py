from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from blog.models import post
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import *
from account.models import User
from django.views.generic import ListView
# Create your views here.


def blog_views(request, **kwargs):
    posts = post.objects.filter(status=1)
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])
    posts = Paginator(posts, 3)

    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)



def blog_single(request, pid):
    posts = get_object_or_404(post, pk=pid)# مربوط به امار ویو
    posts.counted_view+=1# مربوط به امار ویو
    posts.save()# مربوط به امار ویو
    context = {'posts': posts}# مربوط به امار ویو
    return render(request, 'blog/blog-single.html', context)# مربوط به امار ویو


def blog_search(request):
    posts = post.objects.filter(status=1)
    if request.method == 'GET':
        posts = posts.filter(content__contains=request.GET.get('s'))
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/blog')
    else:
        return HttpResponseRedirect('/blog')


class Authorlist(ListView):
    paginate_by = 5
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.post.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context

