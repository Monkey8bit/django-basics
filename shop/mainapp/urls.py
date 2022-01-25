from django.urls import path
import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.product, name='index'),
    path('<int:pk>/',  mainapp.product, name='category'),
]
