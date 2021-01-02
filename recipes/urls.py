from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('profile/<int:user_id>', views.profile_view, name='profile'),
    path('favorites', views.favorite_view, name='favorite'),
    path('favorites/<int:recipe_id>', views.favorite_delete, name='delete_favorite'),
    path('subscriptions', views.subscriptions, name='subscriptions'),
    path('subscriptions/<int:author_id>', views.delete_subscription, name='followers_delete'),
    path('followers/', views.followers, name='followers'),
    path('new/', views.new_recipe, name='recipe_new'),
    path('recipes/<int:recipe_id>', views.recipe_item, name='recipe_view'),
    path('recipes/<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    path('recipes/<int:recipe_id>/delete', views.recipe_delete, name='recipe_delete'),
    path('purchases', views.purchase, name='purchases'),
    path('purchases/<int:recipe_id>', views.purchase_delete, name='delete_purchase'),
    path('shoplist', views.send_shop_list, name='shoplist'),
    path('ingredients/', views.get_ingredients, name='ingredients'),
]
