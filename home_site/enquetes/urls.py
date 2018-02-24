from django.urls import path

from . import views

from django.conf.urls import url, include


from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'enquetes', views.EnqueteViewSet)
router.register(r'respostas', views.RespostaViewSet)

app_name = 'enquetes'

urlpatterns = [
    # API
    url(r'^api/', include(router.urls)),
    # Browser Version REST
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetalheView.as_view(), name='detalhe'),
    path('<int:pk>/resultado/', views.ResultadoView.as_view(),
         name='resultado'),
    path('<int:enquete_id>/votar/', views.votar, name='votar'),
]
