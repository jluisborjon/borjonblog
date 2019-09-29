from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import datetime, date
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

""" Class representing an ArticleForm """
class Article(models.Model):
    CHOICES_IN_CATEGORY = (
        ('Para la Salud', 'Para la Salud'),
        ('Superación Personal','Superación Personal'),
        ('Administración', 'Administración'),
        ('Espiritualidad', 'Espiritualidad'),
        ('Novelas', 'Novelas'),
        ('Anécdotas de mi Tierra', 'Anécdotas de mi Tierra'),
    );
    title = models.CharField(max_length=255)
    body = RichTextUploadingField()
    draft = models.BooleanField()
    category = models.CharField(max_length=255, choices=CHOICES_IN_CATEGORY, default='Administracion')
    published_date = models.DateField()
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pictures', default=1)

    """Defined clean/validation """
    def clean(self):
        if len(self.body) < 2:
            raise ValidationError('The body must be more than one character.')
        elif self.draft and self.published_date < date.today():
            raise ValidationError('If this is a draft, the publish date must be in the future.')

    def __str__(self):
        return "\"{}\" Por {}\n, {}\n ".format(self.title, self.author, self.published_date)


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['author', 'title', 'category', 'body', 'draft', 'published_date']

""" Class representing a CommentForm """
class Comment(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        widgets = {'article': forms.HiddenInput()}
        fields = ['name', 'message', 'article']
