# Generated by Django 3.2.14 on 2022-07-24 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20220724_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagequestion',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.question'),
        ),
    ]