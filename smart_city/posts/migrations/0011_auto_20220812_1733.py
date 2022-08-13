# Generated by Django 3.2.14 on 2022-08-12 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_articlereview_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlereview',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.articlereview'),
        ),
        migrations.AlterField(
            model_name='newsreview',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.newsreview'),
        ),
        migrations.AlterField(
            model_name='questionreview',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.questionreview'),
        ),
    ]
