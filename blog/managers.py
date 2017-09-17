from django.db import models
from django.utils import timezone

from blog.constants import DRAFT, PUBLISHED

'''
class PublishedManager(models.Manager):

    def published(self):
        now = timezone.now()
        return self.get_queryset().filter(status=PUBLISHED,
            publish_date__lte=now)


class RelatedManager(models.Manager):

    def related(self):
        now = timezone.now()
        return self.get_queryset().filter(article__status=PUBLISHED,
            article__publish_date__lte=now).distinct()
'''

class PublishedQuerySet(models.QuerySet):

    def published(self):
        now = timezone.now()
        return self.filter(status=PUBLISHED, publish_date__lte=now)


class RelatedQuerySet(models.QuerySet):

    def related(self):
        now = timezone.now()
        return self.filter(article__status=PUBLISHED,
            article__publish_date__lte=now).distinct()
