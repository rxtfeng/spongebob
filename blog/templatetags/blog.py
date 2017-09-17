from markdown import markdown

from django import template
from django.conf import settings
from django.db.models import Count
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


from blog.models import Article, Tag, Category


register = template.Library()


@register.simple_tag(takes_context=True)
def get_recent_articles(context, number=settings.NUM_RECENT_POSTS):
    if context['request'].user.is_superuser:
        return Article.objects.all()[:number]
    else:
        return Article.objects.published()[:number]


@register.simple_tag(takes_context=True)
def get_all_tags(context):
    if context['request'].user.is_superuser:
        return Tag.objects.all()
    else:
        return Tag.objects.related()


@register.simple_tag(takes_context=True)
def get_all_categories(context):
    if context['request'].user.is_superuser:
        return Category.objects.annotate(num_articles=Count('article'))
    else:
        return Category.objects.related().annotate(num_articles=Count('article'))


@register.simple_tag(takes_context=True)
def get_all_archives(context):
    if context['request'].user.is_superuser:
        return Article.objects.dates('publish_date', 'month', order='DESC')
    else:
        return Article.objects.published().dates('publish_date',
            'month', order='DESC')


@register.inclusion_tag('blog/include/pagination.html', takes_context=True)
def pagination(context):
    is_paginated = context.get('is_paginated')
    if is_paginated is None:
        return None
    else:
        page, paginator = context.get('page_obj'), context.get('paginator')
        page_number = page.number
        page_totals = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            left = []
            if page_totals > 3:
                right = page_range[page_number:page_number+2]
            else:
                right = page_range[page_number:]
        elif page_number == page_totals:
            right = []
            if page_totals > 3:
                left = page_range[page_number-3:page_number-1]
            else:
                left = page_range[:page_number-1]
        else:
            left = page_range[page_number-2]
            right = page_range[page_number]
        left = [left] if isinstance(left, int) else left
        right = [right] if isinstance(right, int) else right
    return {'left': left, 'right': right, 'current': page_number}


@register.filter(is_safe=True, name='markdown')
@stringfilter
def markdown_filter(value):
    content = markdown(value, ['extra', 'admonition', 'pymdownx.tasklist',
        'pymdownx.arithmatex'])
    return mark_safe(content)
