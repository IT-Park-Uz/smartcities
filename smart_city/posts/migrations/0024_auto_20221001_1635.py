# Generated by Django 3.2.14 on 2022-10-01 11:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0023_merge_0022_auto_20220921_0925_0022_auto_20220927_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='posts.Tags'),
        ),
        migrations.AlterField(
            model_name='article',
            name='user_liked',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_liked_a', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='news',
            name='saved_collections',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_saved_n', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='posts.Tags'),
        ),
        migrations.AlterField(
            model_name='news',
            name='user_liked',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_liked_n', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='saved_collections',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_saved_q', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='posts.Tags'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user_liked',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_liked_q', to=settings.AUTH_USER_MODEL),
        ),
    ]
