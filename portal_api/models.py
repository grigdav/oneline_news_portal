from django.db import models

from ckeditor.fields import RichTextField


class NewsCategory(models.Model):
    '''
    Class with News categories.
    '''
    category_id = models.AutoField(db_column='category_id', primary_key=True)
    category_name = models.CharField(max_length=120, blank=True, null=False)

    def __str__(self):
        return str(self.category_name)

    class Meta:
        app_label = 'portal_api'
        managed = True
        db_table = 'news_category'
        verbose_name_plural = 'Category of news'


class News(models.Model):
    '''
    News class with main information about user and two relationship:
        ManyToMany - to relate main news category,
        ForeinKey -  to relate other categories.
    news_title = cant be uniq model PK autogenerate
    news_content = use ckeditor.fields.RichTextField() # for more information\
    see here https://pypi.org/project/django-ckeditor/3.6.2.1/ 
    news_create_time = auto_generate on Yerevan UTC+4 
    '''
    news_title = models.CharField(primary_key=True, db_column='title', max_length=255, blank=True, null=False)
    news_content = RichTextField(db_column='content', blank=True, null=True)
    news_category = models.ManyToManyField(NewsCategory, related_name='news_category', db_column='category', default='')
    news_main_category = models.ForeignKey(NewsCategory, related_name='news_main_category', db_column='main_category',\
                        on_delete=models.CASCADE, null=False)
    news_create_time = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(News, self).__init__( *args, **kwargs)

    def __str__(self):
        return str(self.news_title)

    def get_categories(self):
        return News.objects.filter(category_id=self.category_id)\
            .values_list('news_main_category__category_name', flat=True)

    class Meta:
        app_label = 'portal_api'
        managed = True
        db_table = 'news'
        verbose_name_plural = 'News'
