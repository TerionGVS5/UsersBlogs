"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from app.forms import PostAddForm, BloggerSelectForm
from app.models import Post, Subscription, Reading
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

class PrivateOfficeView(LoginRequiredMixin, View):
    template_name='app/private_office.html'
    login_url = '/login/'
    title='Добро пожаловать в личный кабинет'
    classform_addpost = PostAddForm
    bloggerform_select = BloggerSelectForm
    def get(self, request):
        form_addpost = self.classform_addpost()
        # Чтобы нельзя было на самого себя подписаться
        bloggers_queryset  = User.objects.exclude(pk=request.user.pk)
        # Чтобы на одного и того же нельзя было более одного раза подписаться
        all_subcription = Subscription.objects.all()
        for sub in all_subcription:
            if sub.user == request.user:
                bloggers_queryset = bloggers_queryset.exclude(pk=sub.blogger.pk)
        form_bloggerselect = self.bloggerform_select(bloggers_queryset=bloggers_queryset)
        posts=Post.objects.all().filter(owner=request.user)
        subs=Subscription.objects.all().filter(user=request.user)
        return render(request,self.template_name, {'title':self.title,'form_addpost':form_addpost, 'posts':posts, 'form_selectblogger':form_bloggerselect, 'subs':subs})
    def post(self,request):
        subs=Subscription.objects.all().filter(user=request.user)
        form_addpost = self.classform_addpost(request.POST)
        # Чтобы нельзя было на самого себя подписаться
        bloggers_queryset  = User.objects.exclude(pk=request.user.pk)
        # Чтобы на одного и того же нельзя было более одного раза подписаться
        all_subcription = Subscription.objects.all()
        for sub in all_subcription:
            if sub.user == request.user:
                bloggers_queryset = bloggers_queryset.exclude(pk=sub.blogger.pk)
        form_bloggerselect = self.bloggerform_select(bloggers_queryset=bloggers_queryset)
        if form_addpost.is_valid():
            get_caption=form_addpost.cleaned_data['caption']
            get_text = form_addpost.cleaned_data['text']
            get_user = request.user
            new_post = Post.objects.create(owner=get_user,caption = get_caption,text = get_text)
            posts=Post.objects.all().filter(owner=request.user)
            return render(request,self.template_name, {'title':self.title,'form_addpost':form_addpost, 'posts':posts, 'form_selectblogger':form_bloggerselect, 'subs':subs})
        else:
            return render(request,self.template_name, {'title':self.title,'form_addpost':form_addpost, 'posts':posts, 'form_selectblogger':form_bloggerselect, 'subs':subs})

@login_required(login_url='/login/')
def deletePostView(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if post.owner == request.user:
        post.delete()
    return HttpResponseRedirect('/private_office')

class MakeSubView(LoginRequiredMixin, View):
    bloggerform_select = BloggerSelectForm
    def post(self,request):
        form_bloggerselect = self.bloggerform_select(request.POST)
        if form_bloggerselect.is_valid():
            get_blogger = form_bloggerselect.cleaned_data['bloggers']
            Subscription.objects.create(user=request.user,blogger = get_blogger)
            return HttpResponseRedirect('/private_office')

@login_required(login_url='/login/')
def unsubView(request,pk):
    get_subscription = get_object_or_404(Subscription, pk=pk)
    if get_subscription.user == request.user:
        # Снятие отметок прочитанности
        posts_this_blogger = Post.objects.all().filter(owner=get_subscription.blogger)
        readings = Reading.objects.all().filter(post__in=posts_this_blogger)
        readings.delete()
        get_subscription.delete()
    return HttpResponseRedirect('/private_office')

class NewsFeedView(LoginRequiredMixin, View):
    template_name='app/news_feed.html'
    login_url = '/login/'
    title='Лента новостей'
    def get(self, request):
        get_bloggers = Subscription.objects.all().filter(user=request.user).values_list('blogger')
        get_posts=Post.objects.all().filter(owner__in=get_bloggers).order_by('time')
        get_readings=Reading.objects.all().filter(reader=request.user).values_list('post')
        arr_readings = []
        for el in get_readings:
            arr_readings.append(el[0])
        return render(request,self.template_name, {'title':self.title, 'posts':get_posts, 'readings':arr_readings})

@login_required(login_url='/login/')
def makeUnreaded(request,pk):
    get_post = get_object_or_404(Post, pk=pk)
    # Если пользователь пытается пометить непрочитанным и так непрочитанный пост
    try:
        get_reading = Reading.objects.get(reader=request.user,post=get_post)
        get_reading.delete()
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/news_feed')
    return HttpResponseRedirect('/news_feed')

@login_required(login_url='/login/')
def makeReaded(request,pk):
    get_post = get_object_or_404(Post, pk=pk)
    # Если пользователь пытается пометить прочитанным и так прочитанный пост
    try:
        get_reading = Reading.objects.get(reader=request.user,post=get_post)
    except ObjectDoesNotExist:
        new_reading = Reading.objects.create(reader=request.user,post=get_post)
        return HttpResponseRedirect('/news_feed')
    return HttpResponseRedirect('/news_feed')