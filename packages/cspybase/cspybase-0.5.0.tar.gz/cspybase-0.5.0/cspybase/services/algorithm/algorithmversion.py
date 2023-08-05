## @package algorithmversion
## Módulo reponsável pela estrutrura da configuração em algoritmos.

from cspybase.services.core.exception import CsPyException
from cspybase.services.core.object import CsPyObject
from cspybase.services.algorithm import CsPyAlgorithmConfiguration


## Classe que representa uma versão de algoritmo.
class CsPyAlgorithmVersion(CsPyObject):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    ## @param info dicionário informativo da versão.
    def __init__(self, algorithm, connection, info):
        super().__init__(connection)
        self._algorithm = algorithm
        self._me = {}
        self._updateme(info)

    ## Consulta o algoritmo associado.
    ## @param self objeto do tipo versão.
    ## @return o algoritmo.
    def getalgorithm(self):
        return self._algorithm

    ## Consulta o nome da versão do algoritmo.
    ## @param self objeto do tipo versão.
    ## @return a descrição.
    def getdescription(self):
        return self._me['description']

    def getallparameters(self):
        params = ()
        cnf = self.getconfiguration()
        grps = cnf.get_groups()
        for grp in grps:
            params = params + grp.get_parameters()
        return params

    ## Consulta o configurador de da versão do algoritmo.
    ## @param self objeto do tipo versão.
    ## @return o configurador
    def getconfiguration(self):
        cnn = self.get_connection()
        path = self._getmypath() + "/configuration"
        info = cnn.get(path)
        return CsPyAlgorithmConfiguration(self, info)

    ## Consulta o identificador da versão do algoritmo.
    ## @param self objeto do tipo versão.
    ## @return o id.
    def getid(self):
        return self._me['id']

    ## Consulta o path de URL de acesso
    ## @param self objeto do tipo versão.
    ## @return path
    def _getmypath(self):
        return self.ge_talgorithms_path() + "/" + self.getalgorithm().get_id() + "/versions/" + self.getid()

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info dicionário informativo
    def _updateme(self, info):
        if info is None:
           raise CsPyException("info for algorithm version cannot be none!")
        # print(info)
        self._me['id'] = info['id']
        self._me['description'] = info['description'] if info.get('description') else ""

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        myid = self.getid()
        algo = self.getalgorithm()
        return "Algorithm version: " + algo.get_name() + " V:" + myid

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()
