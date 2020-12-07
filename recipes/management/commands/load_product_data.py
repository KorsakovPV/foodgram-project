from django.core.management.base import BaseCommand
from recipes.models import Product
import csv
class Command(BaseCommand):
    help = 'Load product data to database'
    def handle(self, *args, **options):
        with open('recipes/fixtures/ingredients.csv') as isfile:
            reader = csv.reader(isfile)
            for row in reader:
                title, unit = row
                Product.objects.get_or_create(title=title, unit=unit)