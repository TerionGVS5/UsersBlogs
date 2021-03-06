"""
Definition of urls for UsersBlogs.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^private_office$', app.views.PrivateOfficeView.as_view(), name='private_office'),
    url(r'^private_office/post_detail/(?P<pk>[0-9]+)/$', app.views.PostDetailView.as_view(), name='post_detail'),
    url(r'^news_feed$', app.views.NewsFeedView.as_view(), name='news_feed'),
    url(r'^news_feed/make_unreaded/(?P<pk>[0-9]+)/$', app.views.makeUnreaded, name='make_unreaded'),
    url(r'^news_feed/make_readed/(?P<pk>[0-9]+)/$', app.views.makeReaded, name='make_readed'),
    url(r'^private_office/delete_post/(?P<pk>[0-9]+)/$', app.views.deletePostView, name='delete_post'),
    url(r'^private_office/unsub/(?P<pk>[0-9]+)/$', app.views.unsubView, name='unsub'),
    url(r'^private_office/makesub$', app.views.MakeSubView.as_view(), name='make_sub'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Войти',
                'year': datetime.now().year,
                
            }
        },

        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
