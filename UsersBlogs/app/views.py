"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from app.forms import PostAddForm
from app.models import Post

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
    def get(self, request):
        form = self.classform_addpost()
        posts=Post.objects.all().filter(owner=request.user)
        return render(request,self.template_name, {'title':self.title,'form':form, 'posts':posts})
    def post(self,request):
        posts=Post.objects.all().filter(owner=request.user)
        form = self.classform_addpost(request.POST)
        if form.is_valid():
            get_caption=form.cleaned_data['caption']
            get_text = form.cleaned_data['text']
            get_user = request.user
            new_post = Post.objects.create(owner=get_user,caption = get_caption,text = get_text)
            return render(request,self.template_name, {'title':self.title,'form':form, 'posts':posts})
        else:
            return render(request,self.template_name, {'title':self.title,'form':form, 'posts':posts})

 