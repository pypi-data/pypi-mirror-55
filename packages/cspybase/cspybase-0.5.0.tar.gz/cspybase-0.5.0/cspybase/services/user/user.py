## @package user
## Módulo responsável pela abstração do conceito de usuário no sistema

from cspybase.services.core.exception import CsPyException
from cspybase.services.core.object import CsPyObject

## Classe que representa um usuário
class CsPyUser(CsPyObject):

    # Construtor
    # @param self objeto
    # @param connection conexão
    # @param dicionário informativo
    def __init__(self, connection, info):
        super().__init__(connection)
        self._me = {}
        self._update_me(info)

    ## Consulta o nome do usuário
    ## @param self objeto do tipo usuário.
    ## @return o nome.
    def get_name(self):
        return self._me['name']

    ## Consulta o identificador do usuário
    ## @param self objeto do tipo usuário.
    ## @return o id.
    def get_id(self):
        return self._me['id']

    ## Consulta o login do usuário
    ## @param self objeto do tipo usuário.
    ## @return o login.
    def get_login(self):
        return self._me['login']

    # Faz busca de dados no servidor
    # @param self objeto.
    def _fetch_data(self):
        info = self.get_connection().get(self.get_users_path() + "/" + self.get_id())
        self._update_me(info)

    # Atualiza estruturas internas com base em um dicionário 
    # @param self objeto.
    # @param info diconário informativo
    def _update_me(self, info):
        if info is None:
           raise CsPyException("info for user cannot be none!")
        self._me['id'] = info['id']
        self._me['name'] = info['name']
        self._me['login'] = info['login']

    # Consulta representação textual.
    # @param self objeto.
    # @return texto
    def __str__(self):
        return "User: " + self.get_name() + " - " + self.get_id()

    # Consulta representação textual.
    # @param self objeto.
    # @return texto
    def __repr__(self):
        return self.__str__()
