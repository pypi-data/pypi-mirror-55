
# A CSBase for Python

Just planning...


## Montagem de programas CLI

```
[user@host] python setup.py develop
```

## Gerando Tag
```
[user@host] ./release.bash
```


## Publicação

Garantir que o twine esteja instalado.
```
[user@host] pip install twine
```

Ir para a tag a ser publicada.
```
[user@host] git checkout tags/0.5.0
```


Comandos:
```
[user@host] rm -fr build dist
[user@host] python setup.py sdist bdist_wheel
[user@host] tar tzf dist/cspybase-1.0.0.tar.gz
[user@host] twine check dist/*
[user@host] twine upload dist/*
```

