from config import celery_app
import requests
from smart_city.posts.models import News, Tags, Theme
import urllib.request
from django.core.files import File
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

response = requests.get('https://it-park.uz/api/newsApi/5')
response_data: list = response.json()["data"]


@celery_app.task()
def get_posts_from_it_park():
    """Get posts from IT-Park every 1 minute."""
    added_news = []
    itpark_user = User.objects.filter(username="itpark").first()
    itpark_tag = Tags.objects.filter(name="IT Park").first()
    itpark_category = Theme.objects.filter(name="Администрирование").first()
    for news in response_data:
        news: dict
        data = {
            "title": news.get("ru")["title"],
            "description": news.get("ru")["content"],
            "extra_data": {"itpark_id": news.get("id")},
            "theme": itpark_category,
            "user": itpark_user if itpark_user else User.objects.all().first()
        }
        if News.objects.filter(
            extra_data__itpark_id=news.get("id")
        ).exists():
            continue
        image = news.get("thumbnail")
        image_name_index = image[::-1].find("/") + 2
        image_name = image[image_name_index:]
        image_path = settings.MEDIA_ROOT + "/cache/" + image_name
        urllib.request.urlretrieve(image, image_path)
        with File(open(image_path, 'rb')) as img:
            news_obj = News(**data)
            news_obj.image.save(image_name, img)
            news_obj.is_active = True
            news_obj.save()
            news_obj.tags.add(itpark_tag)
            added_news.append(news_obj)
    return added_news
