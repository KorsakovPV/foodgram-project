from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from users.models import User


class Product(models.Model):
    """Модель для хранения ингредиентов (продуктов)."""

    title = models.CharField(max_length=255, verbose_name='Название продукта')
    unit = models.CharField(max_length=64, verbose_name='Единицы измерения')

    def __str__(self):
        return '{title}, {unit}'.format(title=self.title, unit=self.unit)


class Tag(models.Model):
    """Модель тегов. Все возможные теги хранятся в этой модели."""

    name = models.CharField(max_length=100, verbose_name='Название тега')
    slug = models.SlugField(verbose_name='Слаг тега')
    colors = models.SlugField(verbose_name='Цвет тега', default='Black')

    def __str__(self):
        return '{name}'.format(name=self.name)


class RecipeManager(models.Manager):
    """Менеджер реализует сортировку по тегам."""

    def tag_filter(self, tags):
        if tags:
            return super().get_queryset().prefetch_related('author',
                                                           'tags').filter(
                tags__slug__in=tags).distinct()
        else:
            return super().get_queryset().prefetch_related('author',
                                                           'tags').all()


class Recipe(models.Model):
    """Модель для хранения рецептов"""

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipe_author')
    name = models.CharField(max_length=255, verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Описание рецепта')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Изображение блюда')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)
    ingredients = models.ManyToManyField(
        Product, through='Ingredient', related_name='recipe_ingredients')
    cook_time = models.PositiveIntegerField(verbose_name='Время приготовления')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Время публикации', db_index=True)

    recipes = RecipeManager()

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Ingredient(models.Model):
    """
    Модель связывает Recipe и Product. Какие ингредиенты (продукты) и сколько
    их нужно для конкретного рецепта.
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_amount')
    ingredient = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='Количество ингредиента')

    class Meta:
        unique_together = ('ingredient', 'amount', 'recipe')

    def __str__(self):
        return '{amount}'.format(amount=self.amount)


class PurchaseManager(models.Manager):
    """Менеджер модели список покупок."""

    def get_purchases_list(self, user):
        """
        Фукция возвращает QuerySet рецептов списка покупок. Если таких рецепров
        нет возвращает пустой лист.
        """

        try:
            return super().get_queryset().get(user=user).recipes.all()
        except ObjectDoesNotExist:
            return []

    def get_user_purchase(self, user):
        """
        Фукция возвращает все подписки пользователя QuerySet экземпляров класса
        Purchase для пользователя. Если подписок нет создает экземпляр класса
        Purchase для пользователя и возвращает его.
        """

        try:
            return super().get_queryset().get(user=user)
        except ObjectDoesNotExist:
            purchase = Purchase(user=user)
            purchase.save()
            return purchase


class Purchase(models.Model):
    """Модель для хранения рецептов выбранных для покупок."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)

    purchase = PurchaseManager()


class FavoriteManager(models.Manager):
    """Менеджер модели избранное."""

    def get_favorites(self, user):
        """
        Фукция возвращает QuerySet рецептов добавленных в избранное. Если таких
        рецепров нет возвращает пустой лист.
        """

        try:
            return super().get_queryset().get(user=user).recipes.all()
        except ObjectDoesNotExist:
            return []

    def get_tag_filtered(self, user, tags):
        """
        Фукция возвращает QuerySet рецептов добавленных в избранное с учетом
        активных тегов. Если таких рецепров нет возвращает пустой лист.
        """

        try:
            recipes = super().get_queryset().get(user=user).recipes.all()
            if tags:
                return recipes.prefetch_related(
                    'author', 'tags'
                ).filter(
                    tags__slug__in=tags
                ).distinct()
            else:
                return recipes.prefetch_related(
                    'author', 'tags'
                ).all()
        except ObjectDoesNotExist:
            return []


    def get_user(self, user):
        """
        Фукция возвращает все подписки пользователя QuerySet экземпляров класса
        Favorite для пользователя. Если ибранных нет создает экземпляр класса
        Favorite для пользователя и возвращает его.
        """

        try:
            return super().get_queryset().get(user=user)
        except ObjectDoesNotExist:
            favorite_user = Favorite(user=user)
            favorite_user.save()
            return favorite_user


class Favorite(models.Model):
    """Модель для хранения рецептов добавленных в избранное."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)

    favorite = FavoriteManager()
