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
    path('categories/', views.category_list, name='category'),
]

