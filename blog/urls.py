from django.conf.urls import url

from blog.views import *


urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='blog_index'),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/$',
        ArchiveListView.as_view(), name='archive_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        ArticleDetailView.as_view(), name='blog_detail'),
    url(r'^tags/(?P<slug>[-\w]+)/$', TagListView.as_view(), name='tag_detail'),
    url(r'^categories/(?P<slug>[-\w]+)/$', CategoryListView.as_view(),
        name='category_detail'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^about/$', AboutView.as_view(), name='about'),
]
