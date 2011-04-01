from django.contrib.syndication.views import Feed
from django.utils import feedgenerator


class PublicationFeed(Feed):

    model = None
    feed_type = feedgenerator.Rss201rev2Feed

    def items(self):
        return self.model.objects.published()[:10]

    def item_pubdate(self, item):
        return item.publication_start_date
