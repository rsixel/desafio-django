from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic


from .models import Enquete, Resposta

# Implementando os ENDPOINTS REST
#
from rest_framework import viewsets, response, status
from rest_framework.views import APIView
import django_filters.rest_framework

from .serializers import *


class IndexView(generic.ListView):
    template_name = 'enquetes/index.html'
    context_object_name = 'ultimas_enquetes'

    def get_queryset(self):
        return Enquete.objects.order_by('-texto')


class DetalheView(generic.DetailView):
    model = Enquete
    template_name = 'enquetes/detalhe.html'


class ResultadoView(generic.DetailView):
    model = Enquete
    template_name = 'enquetes/resultado.html'


def votar(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id)

    try:
        resposta = request.POST['resposta']
        resposta_selecionada = enquete.resposta_set.get(
            pk=resposta)
    except (KeyError):

        return render(request, 'enquetes/detalhe.html', {
            'enquete': enquete,
            'error_message': "Você não selecionou nenhuma das opções.",
        })
    else:
        # TODO : Fila de votos
        resposta_selecionada.votos += 1
        resposta_selecionada.save()

        return HttpResponseRedirect(
            reverse('enquetes:resultado', args=(enquete.id,)))


# REST
class EnqueteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Enquetes to be viewed or edited.
    """
    queryset = Enquete.objects.all()
    serializer_class = EnqueteSerializer


class RespostaViewSet(viewsets.ModelViewSet):
    """
    View used by Respostas API
    """
    queryset = Resposta.objects.all()
    serializer_class = RespostaSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class RespostasViewSet(viewsets.ModelViewSet):
    """
    View used by Respostas API
    """
    serializer_class = RespostasSerializer

    def get_queryset(self):
        return Enquete.objects.get(pk=self.kwargs['enquete_pk']).respostas

    def create(self, request, enquete_pk):

        serializer = RespostasSerializer(data=request.data,
                                         context={'enquete_pk': enquete_pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data,
                                 status=status.HTTP_201_CREATED,
                                 headers=headers)


class VotoView(APIView):

    def post(self, request, resposta_pk):
        resposta = Resposta.objects.get(pk=resposta_pk)
        resposta.voto += 1

        resposta.save()

        return response.Response({"votos": resposta.voto},
                                 status=status.HTTP_201_CREATED,
                                 headers=headers)
