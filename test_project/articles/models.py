from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    publication_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)


class Note(models.Model):

    article = models.ForeignKey(Article)
    content = models.TextField()
    is_active = models.BooleanField(default=True)


class Image(models.Model):

    article = models.ForeignKey(Article)
    title = models.CharField(max_length=100)
    file = models.ImageField(upload_to='articles')
