from django import forms
from django.forms import CharField, PasswordInput, Form, BooleanField
from blog.models import ArticleForm, RichTextField
from datetime import datetime, date

"""Defined Login Form and field clean/validation """
class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

"""Defined Article Form and field clean/validation """
class ArticleForm(forms.ModelForm):
    CHOICES = (
        ('Para la Salud', 'Para la Salud'),
        ('Superación Personal','Superación Personal'),
        ('Administración', 'Administración'),
        ('Espiritualidad', 'Espiritualidad'),
        ('Novelas', 'Novelas'),
        ('Anécdotas', 'Anécdotas'),
    )
    category = forms.ChoiceField(choices=CHOICES)
    title = CharField(max_length=255)
    body = RichTextField()
    draft = BooleanField()
    published_date = forms.DateField()
    author = CharField(max_length=255)
