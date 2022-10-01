# Generated by Django 3.2.14 on 2022-10-01 17:55

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0025_news_extra_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserUploadImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='UserUploadImage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Question/%y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='article',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='ss'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='ss'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='sss'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ImageQuestion',
        ),
    ]
