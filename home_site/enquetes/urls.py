from django.urls import path

from . import views


app_name = 'enquetes'

urlpatterns = [

    path('', views.index, name='index'),
    path('<int:enquete_id>/', views.detalhe, name='detalhe'),
    path('<int:enquete_id>/resultado/', views.resultado, name='resultado'),
    path('<int:enquete_id>/votar/', views.votar, name='votar'),
]
