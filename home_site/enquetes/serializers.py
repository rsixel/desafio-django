from .models import Enquete, Resposta
from rest_framework import serializers


class EnqueteSerializer(serializers.ModelSerializer):
    resposta_set = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Resposta.objects.all())

    class Meta:
        model = Enquete
        fields = (
            'id',
            'texto'
        )


class RespostaSerializer(serializers.ModelSerializer):
    Enquete_id = serializers.ReadOnlyField(source='enquete.pk')

    class Meta:
        model = Resposta
        fields = (
            'id',
            'opcao',
            'votos',
            'enquete_id',
        )
