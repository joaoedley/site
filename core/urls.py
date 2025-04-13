from django.urls import path
from .views import HomeView, AboutView, profile_view, custom_admin_view, ContatoView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('profile/', profile_view, name='profile'),
    path('sobre/', AboutView.as_view(), name='about'),
    path('contato/', ContatoView.as_view(), name='contato'),
]