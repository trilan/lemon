from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from lemon.publications.managers import PublicationManager


class Publication(models.Model):
    
    """
    This abstract model provides publication-specific fields and tools.
    """

    author = models.ForeignKey(
        User, null=True, editable=False, verbose_name=_('author'),
        related_name='%(app_label)s_%(class)s_set')
    enabled = models.BooleanField(
        _('enabled'), default=True, db_index=True,
        help_text=_("If not set, publication is hidden from visitors anyway."))
    publication_start_date = models.DateTimeField(
        _('publication start date'), default=timezone.now, db_index=True,
        help_text=_("Publication will be visible to visitors starting from "
                    "this date."))
    publication_end_date = models.DateTimeField(
        _('publication end date'), null=True, blank=True, db_index=True,
        help_text=_("Publication will be visible to visitors due to this date"
                    " if set."))

    objects = PublicationManager()

    class Meta:
        abstract = True
        ordering = ['-publication_start_date']
