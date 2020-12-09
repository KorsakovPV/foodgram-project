from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe, Tag, Purchase, Favorite


def _extend_context(context, user):
    context['purchase_list'] = Purchase.purchase.get_purchases_list(user)
    context['favorites'] = Favorite.favorite.get_favorites(user)
    return context

@require_GET
#TODO убрать
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
    return render(request, 'recipes/index.html', context={'username': request.user.username})