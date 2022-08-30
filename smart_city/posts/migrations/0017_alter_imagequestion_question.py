# Generated by Django 3.2.14 on 2022-08-30 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_auto_20220830_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagequestion',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_images', to='posts.question'),
        ),
    ]