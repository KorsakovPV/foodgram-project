from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('profile/<int:user_id>', views.profile_view, name='profile_view'),
    path('favorites', views.favorite_view, name='favorite_view'),
    path('favorites/<int:recipe_id>', views.favorite_delete,
         name='favorite_delete'),
    path('subscriptions', views.subscriptions, name='subscriptions'),
    path('subscriptions/<int:author_id>', views.subscription_delete,
         name='subscription_delete'),
    path('followers/', views.followers_view, name='followers_view'),
    path('new/', views.new_recipe_view, name='recipe_new_view'),
    path('recipes/<int:recipe_id>', views.recipe_item_view,
         name='recipe_view'),
    path('recipes/<int:recipe_id>/edit', views.recipe_edit_view,
         name='recipe_edit_view'),
    path('recipes/<int:recipe_id>/delete', views.recipe_delete,
         name='recipe_delete'),
    path('purchases', views.purchase_view, name='purchases_view'),
    path('purchases/<int:recipe_id>', views.purchase_delete,
         name='purchase_delete'),
    path('shoplist', views.send_shop_list, name='shoplist'),
    path('ingredients/', views.get_ingredients, name='ingredients'),
]
