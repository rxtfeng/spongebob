from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from blog.constants import DRAFT, PUBLISHED
from blog.forms import ContactForm
from blog.models import Article, Category, Tag


class ArticleListView(ListView):

    template_name = 'blog/index.html'
    paginate_by = settings.PAGE_SIZE
    model = Article
    context_object_name = 'article_list'

    def get_queryset(self):
        queryset = super(ArticleListView, self).get_queryset()

        return queryset if self.request.user.is_superuser else queryset.published()


class ArchiveListView(ArticleListView):

    def get_queryset(self):
        queryset = super(ArchiveListView, self).get_queryset()

        return queryset.filter(publish_date__year=self.kwargs.get('year'),
            publish_date__month=self.kwargs.get('month'))


class TagListView(ArticleListView):

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        if self.request.user.is_superuser:
            queryset = tag.article_set.all()
        else:
            queryset = tag.article_set.published()

        return queryset


class CategoryListView(ArticleListView):

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        if self.request.user.is_superuser:
            queryset = category.article_set.all()
        else:
            queryset = category.article_set.published()

        return queryset


class ArticleDetailView(DetailView):

    template_name = 'blog/single.html'
    model = Article
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = super(ArticleDetailView, self).get_queryset()
        if self.request.user.is_superuser:
            queryset = queryset.filter(
                publish_date__year=self.kwargs.get('year'),
                publish_date__month=self.kwargs.get('month'),
                publish_date__day=self.kwargs.get('day'))
        else:
            queryset = queryset.published().filter(
                publish_date__year=self.kwargs.get('year'),
                publish_date__month=self.kwargs.get('month'),
                publish_date__day=self.kwargs.get('day'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context.update({'detail': True})

        return context


class SearchView(ArticleListView):

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            if self.request.user.is_superuser:
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(tags__title__icontains=query) |
                    Q(categories__title__icontains=query)).order_by('id')
            else:
                queryset = queryset.published().filter(
                    Q(title__icontains=query) |
                    Q(tags__title__icontains=query) |
                    Q(categories__title__icontains=query)).order_by('id')

        return queryset.distinct()


class ContactView(FormView):

    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = '/blog/'

    def form_valid(self, form):
        form.save()
        return super(ContactView, self).form_valid(form)


class AboutView(TemplateView):

    template_name = 'blog/about.html'
