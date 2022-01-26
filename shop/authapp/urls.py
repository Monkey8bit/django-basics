from django.urls import path
from . import views as authapp


app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/',  authapp.logout, name='logout'),
    path('registration/', authapp.registration, name='registration'),
    path('edit/', authapp.edit, name='edit'),
]
