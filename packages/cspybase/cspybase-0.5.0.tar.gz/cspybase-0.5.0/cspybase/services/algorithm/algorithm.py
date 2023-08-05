## @package algorithm
## Módulo reponsável pela estrutrura de algoritmos.

from cspybase.services.core.object import CsPyObject
from cspybase.services.user.user import CsPyUser
from cspybase.services.core.exception import CsPyException
from cspybase.services.algorithm import CsPyAlgorithmVersion

## Classe que representa um algoritmo.
class CsPyAlgorithm(CsPyObject):
    
    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    ## @param info dicionário informativo do algoritmo.
    def __init__(self, connection, info):
        super().__init__(connection)
        self._me = {}
        self._versions = ()
        self._update_me(info)

    ## Consulta o nome do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return o nome.
    def get_name(self):
        return self._me['name']

    ## Consulta o identificador do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return o id.
    def get_id(self):
        return self._me['id']

    ## Consulta o usuário criador do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return o usuário.
    def get_creator(self):
        return self._me['creator']

    ## Consulta a última versão do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return a versão.
    def get_last_version(self):
        return self._me['lastversion']

    ## Consulta versões do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return as versões.
    def get_versions(self):
        return self._me['versions']

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info dicionário informativo
    def _update_me(self, info):
        if info is None:
           raise CsPyException("info for algorithm cannot be none!")
        self._me['id'] = info['id']
        self._me['name'] = info['name']
        cnn = self.get_connection()
        self._fill_me(info, 'creator', 'whoCreated', lambda infovalue: CsPyUser(cnn, infovalue))
        self._fill_me(info, 'lastversion', 'lastVersion', lambda infovalue: CsPyAlgorithmVersion(self, cnn, infovalue))
        self._update_versions(info.get('versions'))
        
    ## Atualiza estruturas internas das versões com base em dicionários
    ## @param self objeto.
    ## @param info dicionários informativos de versões
    def _update_versions(self, infos):
        versions = []
        if infos is not None:
           for info in infos:
               versions.append(CsPyAlgorithmVersion(self, self.get_connection(), info))
        self._me['versions'] = tuple(versions)


    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        myid = self.get_id()
        name = self.get_name()
        creator = self.get_creator()
        return "Algorithm: " + name + " - " + myid + " (Creator: " + str(creator) + ") " + "versions: " + str(self.get_versions())

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()
