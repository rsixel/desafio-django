from .models import Enquete, Resposta
from rest_framework import serializers


class EnqueteSerializer(serializers.ModelSerializer):
    respostas = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Resposta.objects.all())

    class Meta:
        model = Enquete
        fields = (
            'id',
            'texto',
            'respostas'
        )


class RespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resposta
        fields = (
            'id',
            'opcao',
            'votos',
        )
