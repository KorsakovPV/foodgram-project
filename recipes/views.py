import json
from urllib.parse import unquote

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import (
    require_GET,
    require_http_methods,
    require_POST
)

from recipes.forms import RecipeForm
from recipes.models import Favorite, Ingredient, Product, Purchase, Recipe, Tag
from users.models import Subscription, User


def extend_context(context, user):
    context['purchase_list'] = Purchase.purchase.get_purchases_list(user)
    context['favorites'] = Favorite.favorite.get_favorites(user)
    context['ingredient_count'] = Ingredient.objects.select_related(
        'ingredient').filter(recipe__purchase__user=user).values(
        'ingredient__title', 'ingredient__unit').annotate(
        total=Sum('amount')).count()
    return context


@require_GET
def index(request):
    tags = request.GET.getlist('tag')
    recipes = Recipe.recipes.tag_filter(tags)
    #TODO 6 - магическая константа. Ничего не значит, не имеет имени, сложна в
    # поддержке (для изменения нужно выкатить новую версию кода), дублируется в
    # нескольких вьюхах.
    # Поэтому:
    # выносим как именованную константу модуля
    # выносим в настройки, чтобы можно было поменять конфигурацию без изменения
    # кода
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'username': request.user.username,
               'title': 'Рецепты',
               'all_tags': Tag.objects.all(),
               'page': page,
               'paginator': paginator,
               }
    user = request.user
    if user.is_authenticated:
        #TODO Меня берут смутные сомнения относительно вот этой части.
        # Если я правильно понимаю, то это нужно, чтобы корректно обрабатывать
        # кнопки "подписаться", "купить" и "избранное". Но в итоге на каждый
        # запрос из базы придут тяжелые ответы с кучей разной информации.
        # Намного легче и проще посылать в базу запросы, которые будут отвечать
        # именно на нужные нам вопросы - "куплен ли", "подписан ли", "в
        # избранном ли". Получается один мини-запрос на рецепт/автора, который
        # отдает только True|False. А пользоваться таким методом будет очень
        # просто, если запихнуть его в темплейт-теги и применять к
        # рецепту/автору/кнопке
        # Советую попробовать и потом поправить в остальных местах тоже
        context = extend_context(context, user)
    return render(request, 'recipes/indexAuth.html', context)


@login_required(login_url='auth/login/')
@require_http_methods(['GET', 'POST'])
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        #TODO закоментированный код точно так же убираем из финальной версии кода,
        # только если он не относится к примеру использования или докстрингам
        # recipe.save()
        form.save()
        # TODO попробовать сделать через форму
        #  Советую вынести в отдельную функцию-хелпер все, что связано с
        #  получением ингридиентов из формы. Ибо это часть, которая связана с
        #  запросом от фронта, а фронт могут переписать. При этом остальная
        #  наша логика работы вьюхи меняться  не должна.
        #  Таким образом мы отдадим всю сериализацию в стороннее место, а код
        #  вьюхи меняться в зависимости от работы фронта не будет
        ingedient_names = request.POST.getlist('nameIngredient')
        ingredient_units = request.POST.getlist('unitsIngredient')
        amounts = request.POST.getlist('valueIngredient')
        products = []
        for i in range(len(ingedient_names)):
            products.append(Product.objects.get(title=ingedient_names[i],
                                                unit=ingredient_units[i]))
        ingredients = []
        for i in range(len(amounts)):
            ingredients.append(
                Ingredient(recipe=recipe, ingredient=products[i],
                           amount=amounts[i]))
        Ingredient.objects.bulk_create(ingredients)
        return redirect('index')
    context = {'username': request.user.username,
               'page_title': 'Создание рецепта',
               'button': 'Создать рецепт',
               'all_tags': Tag.objects.all(),
               'form': form,
               }
    user = request.user
    if user.is_authenticated:
        context = extend_context(context, user)
    return render(request, 'recipes/formRecipe.html', context)


@login_required(login_url='auth/login/')
@require_http_methods(["GET"])
def get_ingredients(request):
    query = unquote(request.GET.get('query'))
    data = list(Product.objects.filter(title__startswith=query).values('title',
                                                                       'unit'))
    return JsonResponse(data, safe=False)


def profile(request, user_id):
    author = get_object_or_404(User, id=user_id)
    tags = request.GET.getlist('tag')
    recipes = Recipe.recipes.tag_filter(tags)
    paginator = Paginator(recipes.filter(author=author), 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'username': request.user.username,
               'title': author.first_name,
               #TODO вижу такое уже второй раз - мб переиспользовать? Например,
               #  темплейт - тег или напрямую в шаблоне запрашивать такую
               #  информацию?
               'all_tags': Tag.objects.all(),
               'page': page,
               'paginator': paginator
               }
    user = request.user
    if user.is_authenticated:
        context = extend_context(context, user)
    return render(request, 'recipes/indexAuth.html', context)


@require_GET
def recipe_item(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe,
        #TODO Аналогично, здесь прям очень ярко. Мы передаем в контекст весь
        # список покупок юзера для того, чтобы увидеть на странице одного
        # рецепта правильную кнопку? Ну такое
        'purchase_list': Purchase.purchase.get_purchases_list(request.user),
        'favorites': Favorite.favorite.get_favorites(request.user)
    }

    return render(request, 'recipes/singlePage.html', context)


# TODO recipe_edit
@login_required(login_url='auth/login/')
@require_http_methods(['GET', 'POST'])
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_view', recipe_id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None,
                          instance=recipe)
        if form.is_valid():
            recipe.ingredients.remove()
            recipe.recipe_amount.all().delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            form.save()
            # TODO не сохраняет ингредиенты загруженные в форму
            #TODO Аналогично, но тут уже вступает в силу принцип
            # "недублирования кода". Очень хотелось бы увидеть
            # переиспользование этого функционала, потому что он достаточно
            # сложный и практически буква в букву дублируется
            ingedient_names = request.POST.getlist('nameIngredient')
            ingredient_units = request.POST.getlist('unitsIngredient')
            amounts = request.POST.getlist('valueIngredient')
            products = []
            for i in range(len(ingedient_names)):
                products.append(Product.objects.get(title=ingedient_names[i],
                                                    unit=ingredient_units[i]))
            ingredients = []
            for i in range(len(amounts)):
                ingredients.append(
                    Ingredient(recipe=recipe, ingredient=products[i],
                               amount=amounts[i]))
            Ingredient.objects.bulk_create(ingredients)

            return redirect('recipe_view', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)
        context = {
            'recipe_id': recipe_id,
            'page_title': 'Редактирование рецепта',
            'button': 'Сохранить',
            'form': form,
            'recipe': recipe
        }
    return render(request, 'recipes/formRecipe.html', context)


@login_required(login_url='auth/login/')
@require_GET
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('index')


@login_required(login_url='auth/login/')
@require_GET
def followers(request):
    try:
        subscriptions = Subscription.objects.filter(
            user=request.user).order_by('pk')
    except ObjectDoesNotExist:
        subscriptions = []
    page_num = request.GET.get('page')
    paginator = Paginator(subscriptions, 6)
    page = paginator.get_page(page_num)
    context = {
        'active': 'subscription',
        'paginator': paginator,
        'page': page,
    }
    user = request.user
    if user.is_authenticated:
        context = extend_context(context, user)
    return render(request, 'recipes/myFollow.html', context)


@login_required(login_url='auth/login/')
@require_http_methods('DELETE')
def delete_subscription(request, author_id):
    author = get_object_or_404(User, id=author_id)
    data = {'success': 'true'}
    follow = Subscription.objects.filter(
        user=request.user, author=author)
    if not follow:
        data['success'] = 'false'
    follow.delete()
    return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_http_methods(['GET', 'POST'])
#TODO Советую подумать над названиями, потому что название вью-функции не
# отображает, что в ней будет происходить. Особенно если учесть, что в ней
# может происходить абсолютно разные действия. Заодно советую глянуть остальные
# функции, просто здесь очень ярко эта проблема видна. что "избранное"? А вот
# "добавить в избранное" или "получить избранное" - уже понятно

def favorite(request):
    if request.method == 'GET':
        tags = request.GET.getlist('tag')
        user = request.user
        recipes = Favorite.favorite.get_tag_filtered(user, tags)
        paginator = Paginator(recipes, 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {'username': request.user.username,
                   'title': 'Избранное',
                   'all_tags': Tag.objects.all(),
                   'page': page,
                   'paginator': paginator
                   }
        user = request.user
        context = extend_context(context, user)
        return render(request, 'recipes/indexAuth.html', context)
    #TODO Тут абсолютно разный код для двух разных запросов. Есть ли смысл
    # держать их в одной функции? ИМХО, они настолько не связаны между собой,
    # что было бы лучше их разделить по разным вью-функциям
    elif request.method == 'POST':
        json_data = json.loads(request.body.decode())
        recipe_id = json_data['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {'success': 'true'}
        favorite = Favorite.favorite.get_user(request.user)
        is_favorite = favorite.recipes.filter(id=recipe_id).exists()
        if is_favorite:
            data['success'] = 'false'
        else:
            favorite.recipes.add(recipe)
        return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_http_methods('DELETE')
def favorite_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    data = {'success': 'true'}
    try:
        favorite = Favorite.favorite.get(user=request.user)
    except ObjectDoesNotExist:
        data['success'] = 'false'
    if not favorite.recipes.filter(id=recipe_id).exists():
        data['success'] = 'false'
    favorite.recipes.remove(recipe)
    return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_http_methods(['GET', 'POST'])
def purchase(request):
    if request.method == 'GET':
        recipes = Purchase.purchase.get_purchases_list(request.user)
        context = {
            'recipes': recipes,
            'active': 'purchase'
        }
        user = request.user
        if user.is_authenticated:
            context = extend_context(context, user)
        return render(request, 'recipes/shopList.html', context)
    elif request.method == 'POST':
        json_data = json.loads(request.body.decode())
        recipe_id = json_data['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase = Purchase.purchase.get_user_purchase(user=request.user)
        data = {
            'success': 'true'
        }
        if not purchase.recipes.filter(id=recipe_id).exists():
            purchase.recipes.add(recipe)
            return JsonResponse(data)
        data['success'] = 'false'
        return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_http_methods('DELETE')
def purchase_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    data = {
        'success': 'true'
    }
    try:
        purchase = Purchase.purchase.get(user=request.user)
    except ObjectDoesNotExist:
        data['success'] = 'false'
    if not purchase.recipes.filter(id=recipe_id).exists():
        data['success'] = 'false'
    purchase.recipes.remove(recipe)
    return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_GET
def send_shop_list(request):
    user = request.user
    ingredients = Ingredient.objects.select_related('ingredient').filter(
        recipe__purchase__user=user).values('ingredient__title',
                                            'ingredient__unit').annotate(
        total=Sum('amount'))
    filename = '{}_list.txt'.format(user.username)
    products = []
    for ingredient in ingredients:
        products.append('{} ({}) - {}'.format(ingredient["ingredient__title"],
                                              ingredient["ingredient__unit"],
                                              ingredient["total"]))
    content = 'Продукт (единицы) - количество \n \n' + '\n'.join(products)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@login_required(login_url='auth/login/')
@require_POST
def subscriptions(request):
    json_data = json.loads(request.body.decode())
    author = get_object_or_404(User, id=json_data['id'])
    is_exist = Subscription.objects.filter(
        user=request.user, author=author).exists()
    data = {'success': 'true'}
    if is_exist:
        data['success'] = 'false'
    else:
        Subscription.objects.create(user=request.user, author=author)
    return JsonResponse(data)


def page_not_found(request, exception):
    return render(
        request,
        'recipes/misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'recipes/misc/500.html', status=500)
