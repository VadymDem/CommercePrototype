from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add/<int:listing_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove/<int:listing_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_render, name='category_render'),
    path('place_bid/<int:listing_id>/', views.place_bid, name='place_bid'),
    path('close_auction/<int:listing_id>/', views.close_auction, name='close_auction'),
    path('add_comment/<int:listing_id>/', views.add_comment, name='add_comment'),
]


