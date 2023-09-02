from django.urls import path
from .views import register_view, login_view, logout_view, code_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', register_view, name='signup'),
    path('check_code/', code_view, name='check_code'),
]
