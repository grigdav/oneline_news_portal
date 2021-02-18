from django.contrib import admin
from .models import *


class CatInline(admin.TabularInline):
    model = News.news_category.through


class NewsAdmin(admin.ModelAdmin):
    model = News
    inlines = [
        CatInline,
    ]
    list_display = ('news_title', 'news_create_time', 'news_main_category', )
    search_fields = ['news_title', 'news_main_category__category_name', ]
    list_filter = ['news_main_category__category_name', 'news_create_time', ]

admin.site.register(News, NewsAdmin)
admin.site.register(NewsCategory)
