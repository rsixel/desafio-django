from .models import Enquete, Resposta
from rest_framework import serializers


class RespostaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resposta
        fields = (
            'id',
            'opcao',
            'votos'
        )


class EnqueteSerializer(serializers.ModelSerializer):
    respostas = RespostaSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Enquete
        fields = (
            'id',
            'texto',
            'ativa',
            'respostas'
        )

    def create(self, validated_data):
        respostas = validated_data.pop('respostas')

        enquete = Enquete.objects.create(**validated_data)

        for item in respostas:
            resposta = Resposta(enquete=enquete, **item)
            resposta.save()

        return enquete
