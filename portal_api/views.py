from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *



class NewsListView(ListView):
    # News base ListView using in HomePage(index)
    # contex have a two objects (News and NewsCategory)
    model = News
    template_name = 'index.html'
    paginate_by = 10
    ordering = ['-news_create_time']
    context_object_name = 'all_news_list'

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['category_list'] = NewsCategory.objects.all()

        list_news = News.objects.all()
        paginator = Paginator(list_news, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            news_paginate = paginator.page(page)
        except PageNotAnInteger:
            news_paginate = paginator.page(1)
        except EmptyPage:
            news_paginate = paginator.page(paginator.num_pages)
        context['news_paginate'] = news_paginate

        return context


class CategoryNewsListView(ListView):
    # News filtered ListView using in Categories Page
    # queryset filtered by news_main_category
    model = News
    template_name = 'news_by_category.html'
    paginate_by = 10
    ordering = ['-news_create_time']
    context_object_name = 'all_news_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryNewsListView, self).get_context_data(**kwargs)
        context['category_list'] = NewsCategory.objects.all()

        list_news = News.objects.\
            filter(news_main_category__category_name=self.kwargs['category'])
        paginator = Paginator(list_news, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            filtered_news_paginate = paginator.page(page)
        except PageNotAnInteger:
            filtered_news_paginate = paginator.page(1)
        except EmptyPage:
            filtered_news_paginate = paginator.page(paginator.num_pages)
        context['filtered_news_paginate'] = filtered_news_paginate        
        return context

    def get_queryset(self):
        return super(CategoryNewsListView, self).get_queryset().filter(
        news_main_category__category_name=self.kwargs['category']
        )


def news_detail(request, title, template_name='news_detail.html'):
    try:
        news = News.objects.filter(news_title=title)
        return render(request, template_name, {'news': news })
    except:
        raise Http404

def custom_404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response

