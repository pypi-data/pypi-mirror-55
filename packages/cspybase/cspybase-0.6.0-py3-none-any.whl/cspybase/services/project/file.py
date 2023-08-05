## @package file
## Módulo responsável pela abstração do conceito de arquivos/diretórios no sistema

import shutil
import urllib.request
import tempfile
import os

from cspybase.services.user.user import CsPyUser
from cspybase.services.core.exception import CsPyException
from cspybase.services.core.object import CsPyObject

## Classe que representa um arquivo ou diretório
class CsPyFile(CsPyObject):

    # Construtor
    # @param self objeto do tipo arquivo/diretório
    # @param connection conexão
    # @param projectid identificador do projeto
    # @param info dicionário informativo dos dados o arquivo/diretório
    def __init__(self, connection, projectid, info):
        super().__init__(connection)
        if info is None:
           raise CsPyException("bad info for file constructor!")
        if projectid is None:
           raise CsPyException("bad projectid for file constructor!")
        self._written = False
        self._tempfile = None
        self._tempfilename = None
        self._projectid = projectid
        self._me = {}
        self._children = []
        self._update_me(info)


    ## Consulta o nome do arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return o nome
    def get_name(self):
        return self._me['name']

    ## Consulta o identificador único do arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return o id
    def get_id(self):
        return self._me['id']

    ## Consulta se o objeto representa um diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return indicativo (True ou False)
    def is_folder(self):
        return self._me['isfolder']

    ## Consulta se o objeto representa um arquivo
    ## @param self objeto do tipo arquivo/diretório
    ## @return indicativo (True ou False)
    def is_file(self):
        return not self.is_folder()

    ## Consulta o identificador único do pai (parent)
    ## @param self objeto do tipo arquivo/diretório
    ## @return o id do diretório pai
    def get_parent_id(self):
        return self._me['parentid']

    ## Consulta o identificador único do projeto a que pertence o arquivo/diretório.
    ## @param self objeto do tipo arquivo/diretório
    ## @return o id do projeto
    def get_project_id(self):
        return self._projectid

    ## Consulta o path do arquivo/diretório dentro do projeto
    ## @param self objeto do tipo arquivo/diretório
    ## @return o path
    def get_path(self):
        return self._me['path']

    ## Consulta o usuário criador do arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return um objeto representativo do usuário.
    def get_creator(self):
        return self._me['creator']

    ## Consulta a descrição do arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    ## @return a descrição textual
    def get_description(self):
        return self._me['description']

    ## Consulta a lista de filhos de um diretório
    ## @param self objeto do tipo diretório
    ## @return a lista de objetos do tipo arquivo/diretório
    def list(self):
        self._check_is_folder()
        self._fetch_data()
        return self._children

    ## Cria um novo diretório dentro do objeto 'self' diretório
    ## @param self objeto do tipo diretório
    ## @param name nome do novo diretório a ser criado.
    ## @return um objeto que representa o novo diretório
    def mkdir(self, name):
        self._check_is_folder()
        newdir = self.get_file(name)
        if newdir is not None:
            if newdir.isfile():
                raise CsPyException("file already exists!")
            else:
                return newdir
        params = {'name': name}
        info = self.get_connection().post(self._get_my_path() + "/folder", params)
        file = CsPyFile(self.get_connection(), self.get_project_id(), info)
        return file

    ## Apaga o arquivo/diretório
    ## @param self objeto do tipo arquivo/diretório
    def delete(self):
        info = self.get_connection().delete(self._get_my_path(), {})

    ## Retorna um filho (com base em um nome) do objeto do tipo diretório
    ## @param self objeto do tipo diretório.
    ## @param name nome a ser pesquisado.
    ## @return o objeto do tipo arquivo/diretório ou None (se não houver)
    def get_file(self, name):
        self._check_is_folder()
        children = self.list()
        for child in children:
            if child.get_name() == name:
               return child
        return None

    ## Retorna um objeto do tipo diretório que representa o pai deste arquivo/diretório.
    ## @param self objeto do tipo arquivo/diretório
    ## @return objeto do tipo diretório
    def get_parent(self):
        pinfo = self.get_connection().get(self._get_parent_path() + "/metadata", {})
        if pinfo is None:
           return None
        info = pinfo.get('file')
        parent = CsPyFile(self.get_connection(), self.get_project_id(), info)
        return parent

    ## Retorna um link associado ao objeto do tipo arquivo/diretório dentro do servidor
    ## @param self objeto do tipo arquivo/diretório
    ## @return um texto com a URL
    def get_link(self):
        self._check_is_not_folder()
        info = self.get_connection().get(self._get_my_path() + "/link", {})
        if info is None:
           return None
        url = info.get('url')
        return url

    ## Faz o download do objeto do tipo arquivo.
    ## @param self objeto do tipo arquivo/diretório
    ## @param filename nome do arquivo aonde será feito o download.
    def download(self, filename):
        self._check_is_not_folder()
        url = self.get_link()
        if url is None:
           return CsPyException("unable do find a link to file")
        with urllib.request.urlopen(url) as response, open(filename, 'wb') as outfile:
             shutil.copyfileobj(response, outfile)

    ## Cria um novo arquivo dentro do objeto do tipo diretório (não faz nada se já existir).
    ## @param self objeto do tipo arquivo/diretório
    ## @param filename nome do arquivo a ser criado.
    ## @return o novo arquivo criado ou já existente
    def touch(self, filename):
        self._check_is_folder()
        file = self.get_file(filename)
        if file is not None:
           return file
        self.get_connection().touch(self._get_my_path(), filename)
        self._fetch_data()
        return self.get_file(filename)

    ## Abre um arquivo dentro do objeto do tipo diretório (cria se não existir)
    ## @param self objeto do tipo diretório
    ## @param filename nome do arquivo a ser aberto
    ## @param accessmode modo de acesso ao arquivo.
    ## @param buffering tamnaho do buffer (opcional)
    def open_file(self, filename, accessmode, buffering = None):
        file = self.touch(filename)
        file.open(accessmode, buffering)
        return file

    ## Abre o arquivo 
    ## @param self objeto do tipo arquivo
    ## @param accessmode modo de acesso ao arquivo.
    ## @param buffering tamnaho do buffer (opcional)
    def open(self, accessmode, buffering = None):
        self._check_is_not_folder()
        parent = self.get_parent()
        parent.touch(self.get_name())

        buffering = 1024 if buffering is None else buffering
        tmpname = tempfile.mktemp()
        tmpfile = open(tmpname, "wb", 1024 * 1024)
        url = self.get_link()
        if url is None:
           return CsPyException("unable do find a link to file")
        with urllib.request.urlopen(url) as response:
             shutil.copyfileobj(response, tmpfile)

        tmpfile.close()

        self._tempfile = open(tmpname, accessmode, buffering)
        self._tempfilename = tmpname

    ## Fecha o arquivo.
    ## @param self objeto do tipo arquivo.
    def close(self):
        if self._tempfile is None or self.is_folder():
           return
        self._tempfile.close()
        self._tempfile = None
        if self._written: 
           self.get_connection().upload(self._get_parent_path(), self._tempfilename, self.get_name())
        os.remove(self._tempfilename)
        self._tempfilename = None

    ## Escreve bytes no arquivo
    ## @param self objeto do tipo arquivo.
    ## @param data dados a serem gravados.
    ## @return número de bytes escritos
    def write(self, data):
        self._written = True
        self._check_opened_file()
        self._check_is_not_folder()
        return self._tempfile.write(data)

    ## Lê bytes do arquivo.
    ## @param self objeto do tipo arquivo.
    ## @param count quantidade de bytes a serem lidos (opcional)
    ## @return número de bytes escritos.
    def read(self, count = -1):
        self._check_opened_file()
        self._check_is_not_folder()
        return self._tempfile.read(count)

    ## Lê uma linha inteira de do objeto arquivo.
    ## @param self objeto do tipo arquivo.
    ## @param size quantidade máxima de bytes a serem lidos (opcional).
    ## @return texto com um '\n' no final da string -- o newline é omitido caso seja a última linha do arquivo.
    def readline(self, size = -1):
        self._check_opened_file()
        self._check_is_not_folder()
        return self._tempfile.readline(size)

    ## Altera a posição corrente de I/O do obejto do tipo arquivo.    
    ## @param self objeto do tipo arquivo.
    ## @param offset desclocament dentro de uma referência (whence).
    ## @param whence referência opcional dentro do arquivo (0, começo do arquivo; 1, posição corrente, 2, fim do arquivo).
    def seek(self, offset, whence = 0):
        self._check_opened_file()
        self._check_is_not_folder()
        return self._tempfile.seek(offset, whence)
    
    ## Consulta a posição corrente de I/O do objeto do tipo arquivo.
    ## @param self objeto do tipo arquivo.
    ## @return a posição
    def tell(self):
        self._check_opened_file()
        self._check_is_not_folder()
        return self._tempfile.tell()

    ## Testa se o arquivo está aberto
    ## @param self objeto.
    ## @throws CsPyException caso o teste falhe.
    def _check_opened_file(self):
        if self._tempfile is None:
           raise CsPyException("This operation is allowed only to opened files!")

    ## Testa se o objeto não é diretório
    ## @param self objeto.
    ## @throws CsPyException caso o teste falhe.
    def _check_is_not_folder(self):
        if self.is_folder():
           raise CsPyException("This operation allowed only to non-directories!")

    ## Testa se o objeto é diretório
    ## @param self objeto.
    ## @throws CsPyException caso o teste falhe.
    def _check_is_folder(self):
        if not self.is_folder():
           raise CsPyException("This operation allowed only to directories!")

    ## Consulta path REST do objeto diretório-pai no servidor
    ## @param self objeto.
    ## @return path
    def _get_parent_path(self):
        return self._get_path(self.get_project_id(), self.get_parent_id())

    ## Consulta path REST do objeto arquivo/diretório no servidor
    ## @param self objeto.
    ## @return path
    def _get_my_path(self):
        return self._get_path(self.get_project_id(), self.get_id())

    ## Consulta path REST no servidor de um projeto/arquivo
    ## @param self objeto.
    ## @param projectid id do projeto.
    ## @param fileid id do arquivo.
    ## @return path
    def _get_path(self, projectid, fileid):
        return "/v1/projects/" + str(projectid) + "/files/" + str(fileid)

    ## Faz busca de dados no servidor
    ## @param self objeto.
    def _fetch_data(self):
        info = self.get_connection().get(self._get_my_path() + "/metadata", {})
        self._update(info)

    ## Atualiza todos dados (internos e dos filhos) com base em dicionário informativo
    ## @param self objeto.
    def _update(self, info):
        finfo = info.get('file')
        self._update_me(finfo)
        cinfos = info.get('content')
        self._update_children(cinfos)

    ## Atualiza dados internos com base em dicionário informativo
    ## @param self objeto.
    def _update_me(self, info):
        if info is None:
           raise CsPyException("bad info for file updateme!")
        myid = info.get('id')
        if myid is None:
           raise CsPyException("no id for file updateme!")

        self._me['id'] = myid
        self._me['name'] = info.get('name')
        self._me['isfolder'] = info.get('isFolder')
        self._me['description'] = info.get('description')
        self._me['underconstruction'] = info.get('isUnderConstruction')
        self._me['path'] = info.get('path')
        self._me['parentid'] = info.get('parentId')
        userinfo = info.get('createdBy')
        if userinfo is not None:
           self._me['creator'] = CsPyUser(self.get_connection(), userinfo)

    ## Atualiza dados dos filhos com base em lista de dicionários informativos
    ## @param self objeto.
    def _update_children(self, infos):
        self._children = [];
        for info in infos:
            if info is not None:
               file = CsPyFile(self.get_connection(), self.get_project_id(), info)
               self._children.append(file)

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        return "File: " + self.get_name() + " - " + self.get_id()

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()



