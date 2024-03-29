from django_seed import Seed
from smart_city.posts.models import News, Theme
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth import get_user_model

User = get_user_model()

seeder = Seed.seeder(locale='ru_RU')


class Command(BaseCommand):
    help = 'Add fake workers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            nargs='?',
            default=5000
        )

    def create_object(self):
        theme = Theme.objects.all().first()
        user = User.objects.all().first()
        obj = News.objects.create(title=seeder.faker.name(),
                                  # image=seeder.faker.image_url(),
                                  theme=theme,
                                  user=user,
                                  is_active=True,
                                  description=seeder.faker.paragraph()
                                  )
        return obj

    def handle(self, *args, **options):
        workers_count = options['count']
        for i in range(workers_count):
            self.create_object()

        self.stdout.write(self.style.SUCCESS(f'{workers_count} news created successfully'))
