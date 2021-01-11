from django import template
from django.db.models import Sum

from recipes.models import Favorite, Purchase, Tag, Ingredient
from users.models import Subscription

register = template.Library()


@register.filter
def url_with_get(request, page):
    """Возвращает ссылку для pagination"""

    query = request.GET.copy()
    query['page'] = page
    return query.urlencode()


@register.filter
def add_color(tag):
    """Возвращает цвет тега"""

    colors = {entry['slug']: entry['colors'] for entry in
              Tag.objects.values('slug', 'colors')}
    return colors[tag.slug]


@register.filter
def addclass(field, css):
    """Возвращает класс CSS"""

    return field.as_widget(attrs={"class": css})


@register.filter
def subtract(number_1, number_2):
    """Возвращает сколько рецептов не отобразилось в форме мои подписки"""

    return int(number_1) - int(number_2)


@register.filter
def get_tags(request):
    """Возврашает список активный тегов"""

    return request.getlist('tag')


@register.filter
def renew_tag_link(request, tag):
    """Возвращает строки необходимые для формирования ссылки тегов"""

    request_copy = request.GET.copy()
    tags = request_copy.getlist('tag')
    if tag.slug in tags:
        tags.remove(tag.slug)
        request_copy.setlist('tag', tags)
    else:
        request_copy.appendlist('tag', tag.slug)
    return request_copy.urlencode()


@register.filter
def is_favorite(recipe, user):
    """Проверяет, находится ли рецепт в избранном."""

    return Favorite.favorite.filter(recipes=recipe, user=user).exists()


@register.filter
def is_purchase(recipe, user):
    """Проверяет, находится ли рецепт в списке покупок."""

    return Purchase.purchase.filter(recipes=recipe, user=user).exists()


@register.filter
def is_subscribe(author, user):
    """Проверяет, находится ли рецепт в списке покупок."""

    return Subscription.objects.filter(author=author, user=user).exists()


@register.filter
def all_tags(value):
    """Возвращает все теги."""

    return Tag.objects.all()


@register.filter
def ingredient_count(user):
    """Возвращает колличество наименований продуктов в списке покупок."""

    return Ingredient.objects.select_related(
        'ingredient').filter(recipe__purchase__user=user).values(
        'ingredient__title', 'ingredient__unit').annotate(
        total=Sum('amount')).count()
