
# A CSBase for Python

Just planning...


## Programas CLI
A instalação (em ambiente de desenvolvimento) é feita com o comando:
```
[user@host] python setup.py develop
```
Ver seção ```entry_points.console_scripts``` no arquivo ```setup.py```
```
[user@host] cs-list-users
```

## Gerando Tag
```
[user@host] ./release.bash
```

## (Re)Criando virtual env

1. Garanta que o mesmo está instalado
2. Por padrão usamos o diretório ```venv```. Garanta que ele não existe.
3. Crie o direorio com o comando ```virtualenv```
4. Ative o mesmo

```
[user@host] sudo pip install virtualenv
[user@host] rm -fr venv
[user@host] virtualenv venv
[user@host] source venv/bin/activate
```

## Publicação

Passos:

* Garantir que o twine esteja instalado.
```
[user@host] pip install twine
```

* Ir para a tag a ser publicada.
```
[user@host] git checkout tags/0.5.0
```

* Executar os comandos de build e upload:
```
[user@host] rm -fr build dist
[user@host] python setup.py sdist bdist_wheel
[user@host] tar tzf dist/cspybase-x.x.x.tar.gz
[user@host] twine check dist/*
[user@host] twine upload dist/*
```

* Voltar para o branch desejado (de desenvolvimento)
```
[user@host] git checkout master
```
