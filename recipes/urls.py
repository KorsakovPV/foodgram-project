from django.urls import path

from recipes import views


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    # path('favorites', views.FavoriteView.as_view(), name='favorite'),
    # path('favorites/<int:recipe_id>', views.delete_favorite,
    path('favorites', views.favorite, name='favorite'),
    path('favorites/<int:recipe_id>', views.favorite_delete, name='delete_favorite'),
#     2 followers я подписан ·
#     5 following на меня подписаны·
    path('followers/', views.get_subscriptions, name='followers'),
#     path('subscriptions', views.subscription, name='subscription'),
#     path('subscriptions/<int:author_id>', views.delete_subscription,
#          name='delete_subscription'),
    path('new/', views.new_recipe, name='recipe_new'),
    path('recipes/<int:recipe_id>', views.recipe_item, name='recipe_view'),
    path('recipes/<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    path('recipes/<int:recipe_id>/delete', views.recipe_delete, name='recipe_delete'),
    # path('purchases', views.PurchaseView.as_view(), name='purchases'),
#     path('purchases/<int:recipe_id>', views.delete_purchase,
#          name='delete_purchase'),
    path('purchases', views.purchase, name='purchases'),
    path('purchases/<int:recipe_id>', views.purchase_delete, name='delete_purchase'),
    path('shoplist', views.send_shop_list, name='shoplist'),
    path('ingredients/', views.get_ingredients, name='ingredients'),
]