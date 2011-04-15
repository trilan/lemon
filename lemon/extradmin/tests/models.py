from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        app_label = 'extradmin'
