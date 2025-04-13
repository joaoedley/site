from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .views import custom_admin_view

urlpatterns = [
    path('', staff_member_required(custom_admin_view), name='custom_admin'),
]