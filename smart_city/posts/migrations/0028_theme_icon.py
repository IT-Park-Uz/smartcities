# Generated by Django 3.2.14 on 2022-10-28 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0027_auto_20221028_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='Themes/%y/%m/%d', verbose_name='Icon'),
        ),
    ]