
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_framework.test import APIClient

from requests.auth import HTTPBasicAuth


# Utilitários de comparação de estruturas de listas de dicionários
def isDict(o):
    return type(o) is dict or o.__class__.__name__ == 'OrderedDict'


def isList(o):
    return type(o) is list or o.__class__.__name__ == 'ReturnList'


def equalDicts(d1, d2):
    for k in d1.keys():
        if k not in d2:
            return False
        else:
            if isDict(d1[k]):
                if not equalDicts(d1[k], d2[k]):
                    return False
            elif isList(d1[k]):
                return equalListDicts(d1[k], d2[k])
            elif d1[k] != d2[k]:
                return False

    return True


def equalListDicts(l1, l2):

    found = False

    if(isList(l1) and isList(l2)):
        for i1 in l1:
            for i2 in l2:
                if isDict(i1) and isDict(i2):
                    if equalDicts(i1, i2):
                        found = True
                        break
            if found:
                break
    return found


class BaseRESTDeveTests(TestCase):
    URL_ENQUETE = 'http://localhost:8000/enquetes/api/enquete/'
    URL_RESPOSTA = 'http://localhost:8000/enquetes/api/resposta/'

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
            self.URL_ENQUETE,
            self.body, format='json')

        return response

    def criaResposta(self):
        resposta = {"id": 4, "opcao": "ek ek ek", "votos": 0}

        response = self.criaEnquete()

        response = self.client.post(
            self.URL_ENQUETE+'1/respostas/',
            resposta, format='json')
        return response, resposta


# Teste onde DEVE acontecer a senteça que dá nome ao método
# e usuário autenticado
class EnquetesRESTAutenticadoDeveTests(BaseRESTDeveTests):

    def setUp(self):
        super().setUp()
        self.client.login(username='testuser', password='testing')
        self.response = self.criaEnquete()

    def test_deve_criar_enquete_via_post_autenticado(self):

        self.assertEquals(self.response.status_code, 201)
        self.assertTrue(equalDicts(self.response.data, self.bodyRetorno))

    def test_deve_retornar_lista_enquete_autenticado(self):
        response = self.client.get(
            self.URL_ENQUETE,
            None, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(equalDicts(response.data[0], self.bodyRetorno))

    def test_deve_retornar_enquete_pelo_id_autenticado(self):
        response = self.client.get(
            self.URL_ENQUETE+'1/',
            None, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(equalDicts(response.data, self.bodyRetorno))

    def test_deve_alterar_enquete_pelo_id_autenticado(self):
        newbody = self.body.copy()
        newbody.pop("respostas")
        newbody["ativa"] = False

        response = self.client.put(
            self.URL_ENQUETE+'1/',
            newbody, format='json')
        self.assertEquals(response.status_code, 200)

    def test_deve_excluir_enquete_pelo_id_autenticado(self):
        responde = self.criaEnquete()

        response = self.client.delete(
            self.URL_ENQUETE+'1/',
            None, format='json')
        self.assertEquals(response.status_code, 204)

# Teste onde NÃO DEVE acontecer a senteça que dá nome ao método e
# Não autenticado


class EnquetesRESTNAODeveNaoAutenticadoTests(BaseRESTDeveTests):
    def setUp(self):
        super().setUp()
        self.response = self.criaEnquete()

    def test_NAO_deve_criar_enquete_via_post_NAO_autenticado(self):

        response = self.criaEnquete()

        self.assertEquals(response.status_code, 401)

    def test_NAO_deve_retornar_lista_enquete_NAO_autenticado(self):
        response = self.client.get(
            self.URL_ENQUETE,
            None, format='json')
        self.assertEquals(response.status_code, 401)

    def test_NAO_deve_retornar_enquete_pelo_id_NAO_autenticado(self):
        response = self.client.get(
            self.URL_ENQUETE+'1/',
            None, format='json')
        self.assertEquals(response.status_code, 401)

    def test_NAO_deve_alterar_enquete_pelo_id_NAO_autenticado(self):
        newbody = self.body.copy()
        newbody.pop("respostas")
        newbody["ativa"] = False

        response = self.client.put(
            self.URL_ENQUETE+'1/',
            newbody, format='json')
        self.assertEquals(response.status_code, 401)

    def test_NAO_deve_excluir_enquete_pelo_id_NAO_autenticado(self):
        responde = self.criaEnquete()

        response = self.client.delete(
            self.URL_ENQUETE+'1/',
            None, format='json')
        self.assertEquals(response.status_code, 401)


# Teste onde DEVE acontecer e o usuário autenticado
class RespostassRESTAutenticadoDeveTests(BaseRESTDeveTests):

    def setUp(self):
        super().setUp()
        self.client.login(username='testuser', password='testing')

    def test_deve_criar_resposta_via_post_autenticado(self):
        response, resposta = self.criaResposta()

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data, resposta)

    def test_deve_retornar_lista_resposta_da_enquete_autenticado(self):
        response, resposta = self.criaResposta()

        response = self.client.get(
            self.URL_ENQUETE + '1/respostas/',
            None, format='json')

        self.assertEquals(response.status_code, 200)

        listaRespostas = self.bodyRetorno.pop('respostas')
        listaRespostas.append(resposta)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(equalListDicts(response.data, listaRespostas))

    def test_deve_retornar_resposta_pelo_id_autenticado(self):
        response, resposta = self.criaResposta()

        response = self.client.get(
            self.URL_RESPOSTA + '4/',
            None, format='json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, resposta)

    def test_deve_alterar_resposta_pelo_id_autenticado(self):
        response, resposta = self.criaResposta()

        update = {"opcao": "Andorinhas brasileiras", "votos": 2}

        response = self.client.put(
            self.URL_RESPOSTA + '1/',
            update, format='json')

        update['id'] = 1

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, update)

    def test_deve_excluir_resposta_pelo_id_autenticado(self):
        response, resposta = self.criaResposta()

        response = self.client.delete(
            self.URL_RESPOSTA + '1/',
            None, format='json')

        self.assertEquals(response.status_code, 204)

    def teste_deve_adicionar_voto_autenticado(self):
        response, resposta = self.criaResposta()

        response = self.client.post(
            self.URL_RESPOSTA + '1/voto/',
            None, format='json')

        self.assertEquals(response.status_code, 201)


# Teste onde DEVE acontecer a senteça que dá nome ao método.
# Não autenticado
class RespostasRESTNAODeveTests(BaseRESTDeveTests):

    def test_NAO_deve_criar_resposta_via_post_NAO_autenticado(self):

        response, resposta = self.criaResposta()

        self.assertEquals(response.status_code, 401)

    def test_NAO_deve_retornar_lista_resposta_NAO_autenticado(self):
        pass

    def test_NAO_deve_retornar_resposta_pelo_id_NAO_autenticado(self):
        pass

    def test_NAO_deve_alterar_resposta_pelo_id_NAO_autenticado(self):
        pass

    def test_NAO_deve_excluir_resposta_pelo_id_NAO_autenticado(self):
        pass
