import os, sys
sys.path.append('/var/www/test_task/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_task.settings'

import django
django.setup()

from newsapi import NewsApiClient
from portal_api.models import *

class NewsCreaterAPI:
    ''' 
    Base NewsCreate Class: used newsapi python module for more\
    information about module you can find here: 
        https://newsapi.org/docs/client-libraries/python
    This module run every 20 minutes on crontab .
    '''
    def __init__(self):
        # this is possible categories which newsapi work
        # for more information : https://newsapi.org/docs/endpoints/top-headlines
        category_list = ['business', 'entertainment', 'general',\
                    'health', 'science', 'sports', 'technology']

        for category_type in category_list:
            self._categoty_type = category_type
            self.create_news(self._categoty_type )

    def is_news(self, title):
        if News.objects.filter(news_title=title).exists():
            return True
        else:
            return False

    def get_news_category(self):
        if NewsCategory.objects.filter(category_name=self._categoty_type)\
            .exists():
            return NewsCategory.objects.get(category_name=self._categoty_type)
        else:
            new_category_create = NewsCategory(category_name=self._categoty_type)
            new_category_create.save()
            return new_category_create

    def create_news(self, cat):
        newsapi = NewsApiClient(api_key='19e3ce8130e8484db038fa34529f297d')
        # get only 15 news if thay exist
        top_headlines = newsapi.get_top_headlines(category=cat,\
                language='en', page=1, page_size=15)

        articles_dict = top_headlines['articles']

        for key, news_dict in enumerate(articles_dict):
            if self.is_news(news_dict["title"]) is True:
                pass
            else:
                #get_or_create new category and return category object
                category = self.get_news_category()
                # news_dict["title"][:250] must be <= news.title
                # news_dict["content"] will slice by 200 chars because we have trial version.
                new_news = News(news_title=news_dict["title"][:250],\
                        news_content=('<img src="{}"> <br> {} '\
                            .format(news_dict["urlToImage"], news_dict["content"])),
                        news_main_category=category)
                new_news.save()
                print(f'{key}  {news_dict["title"], news_dict["content"], news_dict["urlToImage"]}')
        print('{} news are created!'.format(cat))

NewsCreaterAPI()