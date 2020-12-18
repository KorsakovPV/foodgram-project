from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Load product data to database'

    def handle(self, *args, **options):
        tag1 = Tag.objects.get_or_create(name='завтрак', slug='breakfast')
        tag2 = Tag.objects.get_or_create(name='обед', slug='lunch')
        tag3 = Tag.objects.get_or_create(name='ужин', slug='dinner')
        queryset = Tag.objects.all()
        print(queryset)
