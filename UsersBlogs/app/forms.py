"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Post, Subscription
from django.contrib.auth.models import User

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class PostAddForm(ModelForm):
    class Meta:
        model = Post
        fields = ['caption','text']
        labels = {
            'caption':'Заголовок',
            'text':'Текст'
            }
        widgets = {
            'caption': forms.TextInput({'class': 'form-control'}),
            'text': forms.Textarea({'class': 'form-control'})
            }

class BloggerSelectForm(forms.Form):
    bloggers = forms.ModelChoiceField(queryset=None, empty_label="(Nothing)", label='Блоггер', widget=forms.Select({'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        try:
            bloggers_queryset = kwargs.pop('bloggers_queryset')
        except KeyError:
            bloggers_queryset = User.objects.all()
        super(BloggerSelectForm, self).__init__(*args, **kwargs)
        self.fields['bloggers'].queryset = bloggers_queryset
