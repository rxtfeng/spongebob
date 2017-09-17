from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from blog.constants import DRAFT, PUBLISHED
from blog.managers import PublishedQuerySet, RelatedQuerySet


class Category(models.Model):

    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    objects = RelatedQuerySet().as_manager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'blog_categories'
        ordering = ['title',]

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog:category_detail', None, {'slug': self.slug})


class Tag(models.Model):

    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    objects = RelatedQuerySet().as_manager()

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        db_table = 'blog_tags'
        ordering = ['title',]

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog:tag_detail', None, {'slug': self.slug})


class Article(models.Model):

    STATUS_CHOICES = ((DRAFT, _('Draft')), (PUBLISHED, _('Published')))

    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique_for_date='publish_date')
    content = models.TextField(_('content'))
    abstract = models.TextField(_('abstract'))
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES,
        default=DRAFT)
    publish_date = models.DateTimeField(_('publish date'), default=timezone.now)
    create_date = models.DateTimeField(_('create date'), auto_now_add=True)
    modify_date = models.DateTimeField(_('modify date'), auto_now=True)
    comment_enable = models.BooleanField(_('comment enable'), default=True)
    categories = models.ManyToManyField(Category, verbose_name=_('categories'),
        blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)

    objects = PublishedQuerySet().as_manager()

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        db_table = 'blog_articles'
        ordering = ['-publish_date',]
        get_latest_by = 'publish_date'

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog:blog_detail', None, {
            'year': self.publish_date.strftime('%Y'),
            'month': self.publish_date.strftime('%m'),
            'day': self.publish_date.strftime('%d'),
            'slug': self.slug})

    @property
    def previous_post(self):
        return self.get_previous_by_publish_date(status=PUBLISHED)

    @property
    def next_post(self):
        return self.get_next_by_publish_date(status=PUBLISHED)


class Message(models.Model):

    username = models.CharField(_('username'), max_length=100)
    email = models.EmailField(_('email'))
    message = models.TextField(_('message'))
    contact_date = models.DateTimeField(_('contact date'), auto_now_add=True)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        db_table = 'blog_message'
        ordering = ['-contact_date']

    def __str__(self):
        return self.email
