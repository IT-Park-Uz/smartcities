# Generated by Django 3.2.14 on 2022-09-11 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_auto_20220904_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlikednews',
            old_name='new',
            new_name='news',
        ),
    ]