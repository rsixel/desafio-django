from django.urls import path

from . import views


app_name = 'enquetes'

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetalheView.as_view(), name='detalhe'),
    path('<int:pk>/resultado/', views.ResultadoView.as_view(),
         name='resultado'),
    path('<int:enquete_id>/votar/', views.votar, name='votar'),
]
