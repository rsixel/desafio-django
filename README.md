# Resposta ao Desafio Python/Django Globoesporte

Esta é a resposta ao [desafio Python/Django](https://github.com/globoesporte/desafio-django) da equipe do (globoesporte.com)[https://github.com/globoesporte].

Sou Ricardo Sixel meu contato é rsixel@gmail.com e pelo [facebook](https://www.facebook.com/rsixel).

## Resumo do desafio

O desafio consiste em desenvolver uma aplicação para criar, editar e deletar enquete.

---

## Endpoints REST

Para executar os endpoints abaixo deve ser declarado no header *Content-Type=application/json* .

|Endpoint|Método|Descrição|Observação|
|--------|------|---------|:----------:|
|/api/enquete|POST|Cria nova enquete com as respostas aninhadas.| Ignora os *id's*.
|/api/enquete|GET|Lista todas as enquete. | |
|/api/enquete/\<id\>|GET|Retorna a Enquete pelo \<id\>. ||
|/api/enquete/\<id\>|PUT|Altera a Enquete pelo \<id\>. ||
|/api/enquete/\<id\>|DELETE|Exclui a Enquete pelo \<id\>. ||
|/api/enquete/\<id\>/respostas|GET|Retorna as Respostas da Enquete pelo \<id\>. ||
|/api/enquete/\<id\>/respostas|POST|Cria Respostas da Enquete dada por \<id\>. ||
|/api/resposta/|GET|Retorna a Lista de Respostas. | |
|/api/resposta/\<id\>|GET|Retorna a Respostas pelo \<id\>. | |
|/api/resposta/\<id\>|PUT|Atualiza a Resposta pelo \<id\>. | |
|/api/resposta/\<id\>|DELETE|Atualiza a Resposta pelo \<id\>. | |
|/api/resposta/\<id\>/voto|POST|Gera um voto para a Resposta à Enquete|O corpo da mensagem deve ser vazio. Não precisa de autenticação |
<br>

### Exemplos de JSON:


- __POST /api/enquete:__

Body do post:

```json
{"texto": "Qual a velocidade de uma andorinha?",
 "respostas": [
                { "opcao":"Andorinhas europeias?"},
                {"opcao":"Andorinhas africanas?"},
                {"opcao":"Ahhhhrg!"}  
              ]
 }

```

- __GET /api/enquete:__

Exemplo URL:

`http://localhost:8000/enquete/api/enquete`
`http://localhost:8000/enquete/api/enquete?ativa=true`


Body de retorno (retorna as Respostas aninhadas):

```json
[
        {       
                "id":1,
                "texto": "Qual a velocidade de uma andorinha?",
                "ativa": true,
                "respostas": [
                { 
                        "id": 1,
                        "opcao": "Andorinhas europeias?",
                        "votos": 0
                },    
                {       
                        "id": 2,
                        "opcao": "Andorinhas africanas?",
                        "votos": 0
                },
                { 
                        "id": 3,
                        "opcao": "Ahhhhrggg!!",
                        "votos": 0
                }
                ]
        },

        {
                "id": 2,
                "texto": "O sábio sabia que o sabiá sabia assobiar ?",
                "ativa": true,
                "respostas": [
                {
                        "id": 4,
                        "opcao": "Sabia",
                        "votos": 5
                },
                {
                        "id": 5,
                        "opcao": "Não sabia",
                        "votos": 4
                }
                ]
        }
]
```


- __GET /api/enquete/\<id\>/respostas:__


Exemplo URL:

`http://localhost:8000/enquete/api/enquete/1/repostas`

Body de retorno (retorna as Respostas aninhadas):

```json
[
        { "id": 1,
        "opcao": "Andorinhas europeias?",
        "votos": 0
        },    
        { "id": 2,
        "opcao": "Andorinhas africanas?",
        "votos": 0
        },
        { "id": 3,
        "opcao": "Ahhhhrggg!!",
        "votos": 0
        }
]
```

## Passos utilizados na solução

- Foi utilizado Ubuntu 17 x64  e VS Code 1.20;
- O *Python 3.6* já vem como default;
- Instalei o PIP, utilizando o método descrito [aqui](https://askubuntu.com/questions/967886/unable-to-install-python-pip-in-ubuntu-17-10;);
- Foi utilizado o *pyreqs* para gerar automaticamente o `requirements.txt`. Foi instalado usando :

        # sudo pip install pipreqs
- Foi utilizado o [guia de Python/Jango](https://globoesporte.gitbooks.io/python-e-django-basico/content/content/posts/primeira-aplicacao-em-django.html) do globoesporte.com para criar o projeto.
