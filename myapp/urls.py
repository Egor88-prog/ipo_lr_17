from django.urls import path
from .views import home, author, about_shop

urlpatterns = [
    path('about/', home, name='home'),
    path('about/author/', author, name='author'),
    path('about/about_shop/', about_shop, name='about_shop')
]
