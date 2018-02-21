# Resposta ao Desafio Python/Django Globoesporte

Esta é a resposta ao [desafio Python/Django](https://github.com/globoesporte/desafio-django) da equipe do (globoesporte.com)[https://github.com/globoesporte].

Sou Ricardo Sixel meu contato é rsixel@gmail.com e pelo [facebook](https://www.facebook.com/rsixel).

## Resumo do desafio

O desafio consiste em desenvolver uma aplicação para criar, editar e deletar enquetes.

---

## Importante

- Seguir a convenção PEP8
- Python 3.6
- Django 1.11 ou superior
- README com as instruções para rodar o projeto
- Entregar [API REST](http://www.django-rest-framework.org/) com EndPoints POST, GET, PUT e DELETE
- O EndPoint para salvar o voto é o unico que não é autenticado
- Admin com campo para busca e filtros
- Arquivo requirements.txt na raiz do projeto com todas as dependências

---

## Bonus

No save dos votos, podemos ter uma carga muito grande de votos. Para solucionar este problema, crie uma fila de votos na memória e descarregue no banco a cada 1 minuto.

View Django template para a enquete (não precisa ficar bonito, mas não pode ser terrivelmente feio)

View Admin com dados interesantes sobre a enquete 

Testes unitários também são bem-vindos

Rodando em ambiente docker e deploy em Heroku ou PythonAnywhere


## Passos utilizados na solução

- Foi utilizado Ubuntu 17 x64  e VS Code 1.20;
- O *Python 3.6* já vem como default;
- Instalei o PIP, utilizando o método descrito [aqui](https://askubuntu.com/questions/967886/unable-to-install-python-pip-in-ubuntu-17-10;);
- Foi utilizado o *pyreqs* para gerar automaticamente o `requirements.txt`. Foi instalado usando :

        # sudo pip install pipreqs
- Utilizei o [guia de Python/Jango](https://globoesporte.gitbooks.io/python-e-django-basico/content/content/posts/primeira-aplicacao-em-django.html) do globoesporte.com para criar o projeto.
