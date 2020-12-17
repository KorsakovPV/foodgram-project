from urllib.parse import unquote

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from django.contrib.auth.decorators import login_required

from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag, Purchase, Favorite, Product, Ingredient


def _extend_context(context, user):
    context['purchase_list'] = Purchase.purchase.get_purchases_list(user)
    context['favorites'] = Favorite.favorite.get_favorites(user)
    return context

@require_GET
#TODO убрать доделать index
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
    return render(request, 'recipes/indexAuth.html', context={'username': request.user.username})

#TODO Доделать new_recipe
# @login_required(login_url='auth/login/')
# @require_http_methods(['GET', 'POST'])
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        ingedient_names = request.POST.getlist('nameIngredient')
        ingredient_units = request.POST.getlist('unitsIngredient')
        amounts = request.POST.getlist('valueIngredient')
        products = []
        for i in range(len(ingedient_names)):
            products.append(Product.objects.get(title=ingedient_names[i], unit=ingredient_units[i]))
        ingredients = []
        for i in range(len(amounts)):
            ingredients.append(Ingredient(recipe=recipe, ingredient=products[i], amount=amounts[i]))
        Ingredient.objects.bulk_create(ingredients)
        return redirect('index')
    return render(request, 'recipes/formRecipe.html', {'form': form})
    # context = {
    #     'active': 'new_recipe',
    #     'page_title': 'Создание рецепта',
    #     'button_label': 'Создать рецепт',
    # }
    # # GET-запрос на страницу создания рецепта
    # if request.method == 'GET':
    #     form = RecipeForm()
    #     context['form'] = form
    #     return render(request, 'recipes/formRecipe.html', context)
    # # POST-запрос с данными из формы создания рецепта
    # elif request.method == 'POST':
    #     form = RecipeForm(request.POST, files=request.FILES or None)
    #     if not form.is_valid():
    #         context['form'] = form
    #         return render(request, 'recipes/formRecipe.html', context)
    #     recipe = form.save(commit=False)
    #     recipe.author = request.user
    #     form.save()
    #     ingedient_names = request.POST.getlist('nameIngredient')
    #     ingredient_units = request.POST.getlist('unitsIngredient')
    #     amounts = request.POST.getlist('valueIngredient')
    #     products = [Product.objects.get(
    #         title=ingedient_names[i],
    #         unit=ingredient_units[i]
    #     ) for i in range(len(ingedient_names))]
    #     ingredients = []
    #     for i in range(len(amounts)):
    #         ingredients.append(Ingredient(
    #             recipe=recipe, ingredient=products[i], amount=amounts[i]))
    #     Ingredient.objects.bulk_create(ingredients)
    #     return redirect('index')

# @login_required(login_url='auth/login/')
# @require_GET
def get_ingredients(request):
    query = unquote(request.GET.get('query'))
    data = list(Product.objects.filter(
        title__startswith=query
    ).values(
        'title', 'unit'))
    return JsonResponse(data, safe=False)

