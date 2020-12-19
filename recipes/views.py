from urllib.parse import unquote

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import (require_GET)

from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag, Purchase, Favorite, Product, Ingredient


def _extend_context(context, user):
    context['purchase_list'] = Purchase.purchase.get_purchases_list(user)
    context['favorites'] = Favorite.favorite.get_favorites(user)
    return context


@require_GET
# TODO убрать доделать index
# @login_required(login_url='login')
def index(request):
    # tags = request.GET.getlist('tag')
    # recipe_list = Recipe.recipes.tag_filter(tags)
    # paginator = Paginator(recipe_list, 6)
    # page_number = request.GET.get('page')
    # page = paginator.get_page(page_number)
    # context = {
    #     'all_tags': Tag.objects.all(),
    #     'page': page,
    #     'paginator': paginator
    # }
    # user = request.user
    # if user.is_authenticated:
    #     context['active'] = 'recipe'
    #     _extend_context(context, user)
    # return render(request, 'index.html', context)
    # return HttpResponse('0\n')#)#.join(output))
    tags = request.GET.getlist('tag')
    recipes = Recipe.recipes.tag_filter(tags)  # all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/indexAuth.html',
                  context={'username': request.user.username,
                           'all_tags': Tag.objects.all(),
                           'page': page,
                           'paginator': paginator
                           })


# TODO Доделать new_recipe
# @login_required(login_url='auth/login/')
# @require_http_methods(['GET', 'POST'])
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        # recipe.save()
        form.save()
        # TODO попробовать сделать через форму
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
    return render(request, 'recipes/formRecipe.html', {'form': form})


# @login_required(login_url='auth/login/')
@require_GET
def get_ingredients(request):
    query = unquote(request.GET.get('query'))
    data = list(Product.objects.filter(title__startswith=query).values('title',
                                                                       'unit'))
    return JsonResponse(data, safe=False)


def profile(request, user_id):
    return HttpResponse('profile {}\n'.format(user_id))


@require_GET
def recipe_item(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/singlePage.html', {'recipe': recipe})
    # return HttpResponse('recipe_item {}\n'.format(recipe_id))


def recipe_edit(request, recipe_id):
    return HttpResponse('recipe_edit {}\n'.format(recipe_id))


def recipe_delete(request, recipe_id):
    return HttpResponse('recipe_delete {}\n'.format(recipe_id))


def get_subscriptions(request):
    return HttpResponse('get_subscriptions\n')


class PurchaseView(View):
    pass


class FavoriteView(View):
    pass
