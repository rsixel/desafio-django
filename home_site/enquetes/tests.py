from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_framework.test import APIClient

from requests.auth import HTTPBasicAuth


class EnquetesRESTTests(TestCase):

    body = {"texto":
            "Qual a velocidade de uma andorinha?",
            "ativa": True,
            "respostas": [
                {"id": 1000, "opcao":
                 "Andorinhas europeias?"},
                {"opcao": "Andorinhas africanas?"},
                {"opcao": "Ahhhhrg!"}
            ]
            }

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(
            'testuser', email='testuser@test.com', password='testing')
        self.user.save()

    def test_NAO_deve_criar_enquete_via_post_nao_autenticado(self):

        response = self.client.post(
            'http://localhost:8000/enquetes/api/enquetes/',
            self.body, format='json')

        self.assertEquals(response.status_code, 401)

    def test_deve_criar_enquete_via_post_autenticado(self):

        self.client.login(username='testuser', password='testing')

        response = self.client.post(
            'http://localhost:8000/enquetes/api/enquetes/',
            self.body, format='json')

        self.assertEquals(response.status_code, 201)
