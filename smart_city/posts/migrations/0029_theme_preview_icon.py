# Generated by Django 3.2.14 on 2022-10-28 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0028_theme_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='preview_icon',
            field=models.FileField(blank=True, null=True, upload_to='Themes/%y/%m/%d', verbose_name='Preview Icon'),
        ),
    ]
