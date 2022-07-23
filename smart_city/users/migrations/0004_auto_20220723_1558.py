# Generated by Django 3.2.14 on 2022-07-23 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220723_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='organization',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Bio'),
        ),
        migrations.AddField(
            model_name='user',
            name='organization_name',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='user',
            name='work_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='work name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
    ]
