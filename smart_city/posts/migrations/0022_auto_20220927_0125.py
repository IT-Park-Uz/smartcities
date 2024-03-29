# Generated by Django 3.2.14 on 2022-09-26 20:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0021_auto_20220921_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='saved_collections',
            field=models.ManyToManyField(null=True, related_name='user_saved_a', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='news',
            name='saved_collections',
            field=models.ManyToManyField(null=True, related_name='user_saved_n', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='saved_collections',
            field=models.ManyToManyField(null=True, related_name='user_saved_q', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tags',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
        migrations.AddField(
            model_name='news',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=False)),
                ('user_read', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
