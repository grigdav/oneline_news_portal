# Generated by Django 2.2.12 on 2021-02-18 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_title',
            field=models.CharField(blank=True, db_column='title', max_length=255, primary_key=True, serialize=False),
        ),
    ]