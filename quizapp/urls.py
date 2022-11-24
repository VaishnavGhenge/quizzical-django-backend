from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.initview, name='initview'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('check_user/', views.check_user, name='check_user'),
    path('update_high_score/', views.update_high_score, name='high_score'),
]
