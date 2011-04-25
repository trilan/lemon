from django.views.generic import (
    ListView, DetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView,
    WeekArchiveView, DayArchiveView, TodayArchiveView, DateDetailView)


class PublishedMixin(object):

    def get_queryset(self):
        queryset = super(PublishedMixin, self).get_queryset()
        return queryset.published()


class PublicationDateMixin(object):

    date_field = 'publication_start_date'


class PublicationListView(PublishedMixin, ListView):
    """Works like ListView but returns only published objects"""


class PublicationDetailView(PublishedMixin, DetailView):
    """Works like DetailView but returns object only if published"""


class PublicationArchiveIndexView(PublicationDateMixin, PublishedMixin,
                                  ArchiveIndexView):
    """
    Works like ArchiveIndexView but returns only published objects and uses
    publication_start_date as date_field
    """


class PublicationYearArchiveView(PublicationDateMixin, PublishedMixin,
                                 YearArchiveView):
    """
    Works like YearArchiveView but returns only published objects and uses
    publication_start_date as date_field
    """


class PublicationMonthArchiveView(PublicationDateMixin, PublishedMixin,
                                  MonthArchiveView):
    """
    Works like MonthArchiveView but returns only published objects and uses
    publication_start_date as date_field
    """


class PublicationWeekArchiveView(PublicationDateMixin, PublishedMixin,
                                 WeekArchiveView):
    """
    Works like WeekArchiveView but returns only published objects and uses
    publication_start_date as date_field
    """


class PublicationDayArchiveView(PublicationDateMixin, PublishedMixin,
                                DayArchiveView):
    """
    Works like DayArchiveView but returns only published objects and uses
    publication_start_date as date_field
    """


class PublicationTodayArchiveView(PublicationDateMixin, PublishedMixin,
                                  TodayArchiveView):
    """
    Works like TodayArchiveView but returns only published objects and uses
    publication_start_date as date_field
    """


class PublicationDateDetailView(PublicationDateMixin, PublishedMixin,
                                DateDetailView):
    """
    Works like DateDetailView but returns object only if published and uses
    publication_start_date as date_field
    """
