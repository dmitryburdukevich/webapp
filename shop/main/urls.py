from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.get_main_page, name="main"),
    path('about-us', views.get_about_us_page, name="about"),

    path('products/', views.get_products_page, name='products'),
    path('products/<slug:slug>/', views.get_specific_product, name='specific_product_url_with_slug'),

    path('categories/', views.get_categories, name='categories'),

    # user
    path('registration/', views.get_registration_page, name='registration'),
    path('login/', views.get_login_page, name='login'),
    re_path(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    re_path(r'^orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('logout/', views.logout_user, name='logout_user'),
    path('user-profile/', views.get_user_profile_page, name='profile')
]