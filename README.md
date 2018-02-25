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

Foram utilizados :

- Ubuntu 17 x64  e VS Code 1.20;
- O *Python 3.6* já vem como default;
- Instalei o PIP, utilizando o método descrito [aqui](https://askubuntu.com/questions/967886/unable-to-install-python-pip-in-ubuntu-17-10;);
- *Pyreqs* para gerar automaticamente o `requirements.txt`. Foi instalado usando :

        # sudo pip install pipreqs
- [Guia de Python/Jango](https://globoesporte.gitbooks.io/python-e-django-basico/content/content/posts/primeira-aplicacao-em-django.html) do globoesporte.com para criar o projeto.
- No frontend foi utilizado Bootstrap versão 4.0. 
- Ao invés do bonus proposto foi feita a integração com servidor de fila via Celery 4.1.0. Esse recurso é muito mais robusto pois não represa votos a serem computados, aumentando a demanda de memória, e nem faz com que a cada 1 minuto o banco seja soterrado por requisições relacionados ao flush.

Foi escolhido utilizar o RabittMQ para garantir assincronismo, integridade, e alta-disponibilidade mas para o Celery essa é apenas uma das escolhas. Para enquetes mais recreativas onde pode haver um grande pico de acessos durante um spot na TV, pode ser usado o Redis em memória que pode ter perda em eventual *crash*. Embora isso possa ocorrer o desempenho teoricamente seria maior, por ser em memória.

## Instruções para instalar e executar

### Pré requisitos


- Deve ser instalado o RabbitMQ como backend para o Celery. Ele rodará como `daemon`. O comando está conforme abaixo:

`# sudo apt-get install rabbitmq-server`

### Instalando a aplicação 

- Clone o projeto do Github no local desejado:

`# git clone https://github.com/rsixel/desafio-django`

- Vá para o diretório raiz do projeto e diretório principal do projeto e instale os requisitos do Python:

`# sudo -H pip install -r requirements.txt`

*Obs: pode ser que no seu ambiente baste executar `pip install -r requirements.txt`* 

- Selecione o diretório do *home_site*:

`# cd home_site`

- Execute o comando para testar os endpoint:

`# python3 manage.py test`

Deverá ver o seguinte resultado:

``` Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......................
----------------------------------------------------------------------
Ran 22 tests in 2.978s

OK
Destroying test database for alias 'default'...
```

### Executando a aplicação

Uma vez na pasta  `home_site` do projeto, devem ser executados os seguintes comandos:

- Executando o *worker* do Celery:

`# celery -A home_site worker -l info`

Esse passo é para demonstração do projeto mas pode ser configurado um *daemon* caso o projeto vá para produção.

- Execute o comando para executar o projeto:

`# python3 manage.py runserver`


- Acesse com o browser o administrador em http://localhost:8000/admin. Será possível clicar em Enquete e visualizar:
     - As opções de filtrar enquetes ativas ou inativas na barra direita;
     - Excluir todas as enquetes;
     - Criar novas enquetes;
     - Buscar enquetes.

- Após cadastrar a as enquetes acesse http://localhost:8000/enquetes 
