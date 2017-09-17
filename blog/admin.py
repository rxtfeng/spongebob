from django.contrib import admin
from django.urls import reverse

from blog.models import Article, Category, Tag, Message


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'publish_date']
    list_filter = ['status', 'publish_date']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    fieldsets = (
        (None,
            {'fields': ('title', 'slug', 'abstract', 'content')}),
        ('Advanced',
            {'classes': ('collapse',), 'fields': (('status', 'comment_enable'), 'categories', 'tags', 'publish_date')}),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class MessageAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'contact_date']
    date_hierarchy = 'contact_date'


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Message, MessageAdmin)

admin.site.site_header = 'Spongebob Administration'
admin.site.site_url = reverse('blog:blog_index')
