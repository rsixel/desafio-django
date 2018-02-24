
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_framework.test import APIClient

from requests.auth import HTTPBasicAuth


class BaseRESTDeveTests(TestCase):
    URL_ENQUETES = 'http://localhost:8000/enquetes/api/enquetes/'
    URL_RESPOSTAS = 'http://localhost:8000/enquetes/api/respostas/'

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

    bodyRetorno = {
        "id": 1,
        "texto":
            "Qual a velocidade de uma andorinha?",
            "ativa": True,
            "respostas": [
                {"id": 1, "opcao":
                 "Andorinhas europeias?", "votos": 0},
                {"id": 2, "opcao": "Andorinhas africanas?", "votos": 0},
                {"id": 3, "opcao": "Ahhhhrg!", "votos": 0}
            ]
    }

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(
            'testuser', email='testuser@test.com', password='testing')
        self.user.save()

    def criaEnquete(self):
        response = self.client.post(
            self.URL_ENQUETES,
            self.body, format='json')

        return response

    def criaResposta(self):
        resposta = {"id": 4, "opcao": "ek ek ek", "votos": 0}

        response = self.criaEnquete()

        response = self.client.post(
            self.URL_ENQUETES+'1/respostas',
            self.body, format='json')
        return response, resposta

    def equalDicts(self, d1, d2):
        for k in d1.keys():
            if k not in d2:
                print(k + ' não encontrada !\n')
                return False
            else:
                if type(d1[k]) is dict:
                    if not self.equalDicts(d1[k], d2[k]):
                        return False
                elif type(d1[k]) is list:
                    found = False
                    for i1 in d1[k]:
                        for i2 in d2[k]:
                            if self.equalDicts(i1, i2):
                                found = True
                                break

                    if not found:
                        return False

                elif d1[k] != d2[k]:
                    return False

        return True


# Teste onde DEVE acontecer a senteça que dá nome ao método
# e usuário autenticado
class EnquetesRESTAutenticadoDeveTests(BaseRESTDeveTests):

    def setUp(self):
        super().setUp()
        self.client.login(username='testuser', password='testing')

    def test_deve_criar_enquete_via_post_autenticado(self):

        response = self.criaEnquete()

        self.assertEquals(response.status_code, 201)
        self.assertTrue(self.equalDicts(response.data, self.bodyRetorno))

    def test_deve_retornar_lista_enquete_autenticado(self):

        responde = self.criaEnquete()

        response = self.client.get(
            self.URL_ENQUETES,
            None, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.equalDicts(response.data[0], self.bodyRetorno))

    def test_deve_retornar_enquete_pelo_id_autenticado(self):
        pass

    def test_deve_alterar_enquete_pelo_id_autenticado(self):
        pass

    def test_deve_excluir_enquete_pelo_id_autenticado(self):
        pass


# Teste onde NÃO DEVE acontecer a senteça que dá nome ao método e
# Não autenticado

class EnquetesRESTNAODeveNaoAutenticadoTests(BaseRESTDeveTests):

    def test_NAO_deve_criar_enquete_via_post_NAO_autenticado(self):

        response = self.criaEnquete()

        self.assertEquals(response.status_code, 401)

    def test_NAO_deve_retornar_lista_enquete_NAO_autenticado(self):
        pass

    def test_NAO_deve_retornar_enquete_pelo_id_NAO_autenticado(self):
        pass

    def test_NAO_deve_alterar_enquete_pelo_id_NAO_autenticado(self):
        pass

    def test_NAO_deve_excluir_enquete_pelo_id_NAO_autenticado(self):
        pass


# Teste onde DEVE acontecer e o usuário autenticado
class RespostassRESTAutenticadoDeveTests(BaseRESTDeveTests):

    def setUp(self):
        super()
        self.client.login(username='testuser', password='testing')

    def test_deve_criar_resposta_via_post_autenticado(self):
        response, resposta = self.criaResposta()

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data, resposta)

    def test_deve_retornar_lista_resposta_autenticado(self):
        pass

    def test_deve_retornar_resposta_pelo_id_autenticado(self):
        pass

    def test_deve_alterar_resposta_pelo_id_autenticado(self):
        pass

    def test_deve_excluir_resposta_pelo_id_autenticado(self):
        pass


# Teste onde DEVE acontecer a senteça que dá nome ao método.
# Não autenticado
class RespostasRESTNAODeveTests(BaseRESTDeveTests):

    def test_NAO_deve_criar_resposta_via_post_nao_autenticado(self):

        response, resposta = self.criaResposta()

        self.assertEquals(response.status_code, 401)

    def test_deve_retornar_lista_resposta_NAO_autenticado(self):
        pass

    def test_deve_retornar_resposta_pelo_id_NAO_autenticado(self):
        pass

    def test_deve_alterar_resposta_pelo_id_NAO_autenticado(self):
        pass

    def test_deve_excluir_resposta_pelo_id_NAO_autenticado(self):
        pass
