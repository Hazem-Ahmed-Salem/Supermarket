from django.urls import path
from . import views
urlpatterns = [
    path('', views.test, name='test'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('next_register/', views.next_register_view, name='next_register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_update_view, name='profile_edit'),
]