## @package algorithmconfiguration
## Módulo reponsável pela estrutrura da configuração em algoritmos.

from cspybase.services.core.exception import CsPyException
from cspybase.services.algorithm.algorithmgroup import CsPyAlgorithmGroup
from cspybase.services.algorithm import CsPyAlgorithmAction


## Classe que representa uma configuração de algoritmo.
class CsPyAlgorithmConfiguration:

    ## Construtor
    ## @param self objeto do tipo configurador
    ## @param version versão de algoritmo associada.
    ## @param info dicionário informativo da versão.
    def __init__(self, version, info):
        if version is None:
           raise CsPyException("Version cannot be none.")        
        self._version = version
        self._groups = ()
        self._actions = ()
        self._me = {}
        self._update_me(info)

    ## Consulta o algoritmo associado ao configurador
    ## @param self objeto do tipo configurador
    ## @return algoritmo
    def get_algorithm(self):
        return self.get_algorithm_version().get_algorithm()

    ## Consulta versão do algoritmo associado ao configurador
    ## @param self objeto do tipo configurador
    ## @return versão do algoritmo
    def get_algorithm_version(self):
        return self._version

    ## Consulta comando do configurador
    ## @param self objeto do tipo configurador
    ## @return comando
    def get_command(self):
        return self._me['command']

    ## Consulta tipo de execução do configurador
    ## @param self objeto do tipo configurador
    ## @return tipo de execução
    def get_execution_type(self):
        return self._me['executiontype']

    ## Consulta indicativo de carga de parâmetros do configurador
    ## @param self objeto do tipo configurador
    ## @return indicativo
    def get_load_parameters(self):
        return self._me['loadparameters']

    ## Consulta grupos de parâmetros do configurador
    ## @param self objeto do tipo configurador
    ## @return lista com os grupos
    def get_groups(self):
        return self._groups

    ## Consulta ações de parâmetros do configurador
    ## @param self objeto do tipo configurador
    ## @return lista com as ações
    def get_actions(self):
        return self._actions

    ## Atualiza estruturas internas com base em um dicionário.
    ## @param self objeto.
    ## @param info dicionário informativo.
    def _update_me(self, info):
        if info is None:
           raise CsPyException("info for algorithm configuration cannot be none!")
        self._me['command'] = info.get('command')
        self._me['executiontype'] = info.get('executionType') if info.get('executionType') is not None else "SIMPLE"
        self._me['loadparameters'] = info.get('loadParameters') if info.get('loadParameters') is not None else False
        self._update_groups(info.get('groups'))
        self._update_actions(info.get('actions'))

    ## Faz atualização interna de grupos.
    ## @param self objeto.
    ## @param infos lista de dicionários informativos.
    def _update_groups(self, infos):
        grps = []
        if infos is not None:
           for info in infos:
               grps.append(CsPyAlgorithmGroup(self, info))
        self._groups = tuple(grps)

    ## Faz atualização interna de ações.
    ## @param self objeto.
    ## @param infos lista de dicionários informativos.
    def _update_actions(self, infos):
        acts = []
        if infos is not None:
           for info in infos:
               acts.append(CsPyAlgorithmAction(self, info))
        self._actions = tuple(acts)

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        version = self.get_algorithm_version()
        return "Algorithm version configuration: " + str(version) + " : " + str(self.get_command())

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()

