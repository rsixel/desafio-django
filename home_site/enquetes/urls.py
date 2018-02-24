from django.urls import path

from . import views

from django.conf.urls import url, include

from rest_framework_nested import routers


router = routers.DefaultRouter()

# ENDPOINTs partindo de 'enquete'
router.register(r'enquete', views.EnqueteViewSet)
enquete_router = routers.NestedSimpleRouter(
    router, r'enquete', lookup='enquete')
enquete_router.register(r'respostas', views.RespostasViewSet,
                        base_name='enquete-respostas')

# ENDPOINTs partindo de 'resposta'
router.register(r'resposta', views.RespostaViewSet)
resposta_router = routers.NestedSimpleRouter(
    router, r'resposta', lookup='resposta')
resposta_router.register(r'voto', views.VotoView,
                         base_name='resposta-voto')

app_name = 'enquetes'

urlpatterns = [
    # API
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(enquete_router.urls)),
    url(r'^api/', include(resposta_router.urls)),
    # Browser Version REST
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    # Django web view URLS
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetalheView.as_view(), name='detalhe'),
    path('<int:pk>/resultado/', views.ResultadoView.as_view(),
         name='resultado'),
    path('<int:enquete_id>/votar/', views.votar, name='votar'),
]
