from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic


from .models import Enquete, Resposta

# Implementando os ENDPOINTS REST
#
from rest_framework import viewsets
import django_filters.rest_framework
from .serializers import EnqueteSerializer, RespostaSerializer


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
    filter_fields = ('votos', 'enquete_id')
