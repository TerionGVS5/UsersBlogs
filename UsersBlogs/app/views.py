"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

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
    def get(self, request):
        return render(request,self.template_name, {'title':self.title})
