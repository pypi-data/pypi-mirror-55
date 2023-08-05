

from cspybase.services.core.access import CsPyAccess
from cspybase.services.algorithm import CsPyAlgorithm

## Classe que representa um acesso bem sucedido a um servidor.
class CsPyAlgorithmAccess(CsPyAccess):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)

    ## Consulta a lista de algoritmos disponíveis para este acesso
    ## @param self objeto do tipo acesso
    ## @return uma tupla com os algoritmos.
    def get_algorithms(self):
        algos = self.get_connection().get(self.ge_talgorithms_path(), {})
        algolist = []
        algoit = iter(algos)
        for algo in algoit:
            algolist.append(CsPyAlgorithm(self.get_connection(), algo))
        return tuple(algolist)

    ## Retorna um algoritmo com base em seu id
    ## @param self objeto do tipo acesso
    ## @param algoid o id a ser pesquisado
    ## @return o algoritmo ou None (caso este não seja encontrado)
    def get_algorithm(self, algoid):
        algos = self.get_algorithms()
        for algo in algos:
            if algo.get_id() == algoid:
                return algo
        return None

