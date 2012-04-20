from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        app_label = 'extradmin'


class Author(models.Model):

    article = models.ForeignKey(Article)
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'extradmin'


class Link(models.Model):

    article = models.ForeignKey(Article)
    url = models.URLField()

    class Meta:
        app_label = 'extradmin'
