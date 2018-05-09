"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Post

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