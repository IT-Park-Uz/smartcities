# Generated by Django 3.2.14 on 2022-08-08 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='number',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
