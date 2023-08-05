## @package project
## Módulo responsável pela abstração do conceito de projetos no sistema

from cspybase.services.user.user import CsPyUser
from cspybase.services.project.file import CsPyFile
from cspybase.services.core.exception import CsPyException
from cspybase.services.core.object import CsPyObject

## Classe que representa um projeto dentro do servidor.
class CsPyProject(CsPyObject):

    # Construtor
    # @param self objeto do tipo arquivo/diretório
    # @param connection conexão
    # @param info dicionário informativo dos dados o arquivo/diretório
    def __init__(self, connection, info):
        super().__init__(connection)
        self._me = {}
        self._update_me(info)

    ## Consulta o nome do projeto.
    ## @param self objeto do tipo projeto.
    ## @return o nome.
    def get_name(self):
        return self._me['name']

    ## Consulta o identificador do projeto.
    ## @param self objeto do tipo projeto.
    ## @return o id.
    def get_id(self):
        return self._me['id']

    ## Consulta o usuário dono do projeto.
    ## @param self objeto do tipo projeto.
    ## @return o usuário.
    def get_owner(self):
        return self._me['owner']

    ## Consulta o diretório-raiz do projeto
    ## @param self objeto do tipo projeto.
    ## @return o diretório.
    def get_root(self):
        info = self.get_connection().get(self.get_projects_path() + "/" + self.get_id() + "/files/root/metadata", {})
        if info is None:
            raise CsPyException("bad info for project root!")
        return CsPyFile(self.get_connection(), self.get_id(), info.get('file'))

    ## Faz busca de dados no servidor
    ## @param self objeto.
    def _fetch_data(self):
        info = self.get_connection().get(self.get_projects_path() + "/" + self.get_id(), {})
        self._update_me(info)

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info dicionário informativo
    def _update_me(self, info):
        if info is None:
            raise CsPyException("info for project cannot be none!")
        self._me['id'] = info['id']
        self._me['name'] = info['name']
        self._me['description'] = info['description']
        self._me['owner'] = CsPyUser(self.get_connection(), info['owner'])

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        name = self.get_name()
        myid = self.get_id()
        return "Project: " + name + " - " + myid + " (Owner: " + str(self.get_owner()) + ")"

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()



