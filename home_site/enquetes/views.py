from django.http import HttpResponse
from django.template import loader

from django.shortcuts import get_object_or_404, render

from .models import Enquete


def index(request):
    ultimas_enquetes = Enquete.objects.order_by('-texto')[:5]
    template = loader.get_template('enquetes/index.html')
    context = {
        'ultimas_enquetes': ultimas_enquetes,
    }
    return HttpResponse(template.render(context, request))


def detalhe(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id)
    return render(request, 'enquetes/detalhe.html', {'enquete': enquete})


def resultado(request, enquete_id):
    response = "You're looking at the results of resposta %s."
    return HttpResponse(response % enquete_id)


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
            reverse('enquetes:resultados', args=(resposta.id,)))
