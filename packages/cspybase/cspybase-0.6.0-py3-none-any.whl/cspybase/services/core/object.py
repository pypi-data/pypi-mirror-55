
from cspybase.services.core.exception import CsPyUnconnectedException

## Classe que representa a mãe de todas as classes que precisam ter associadas
## a si uma conexão ao servidor (arquivos, projetos etc). Também possui um construtor
## que inicializa a conexão  e métodos para obtenção de constantes (prefixos de URL
## de acesso a entidades do servidor).
class CsPyObject:

    ## Construtor
    ## @param self objeto 
    ## @param connection conexão previamente estabelecida (verifica se a mesma está online)
    ## @throws CsPyUnconnectedException no caso da conexão não estar estabelecida.
    def __init__(self, connection):
        if not connection.is_connected():
           raise CsPyUnconnectedException() 
        self._projectspath = "/v1/projects"
        self._userspath = "/v1/users"
        self._algorithmspath = "/v1/algorithms"
        self._jobspath = "/v1/jobs"
        self._jobspullpath = self._jobspath + "/pull"
        self._jobscancelpath = self._jobspath + "/operation/cancel"
        self._connection = connection


    ## Consulta o path da URL para acesso à dados de projetos
    ## @param self objeto
    ## @return path
    def get_projects_path(self):
        return self._projectspath


    ## Consulta o path da URL para acesso à dados de algoritmos
    ## @param self objeto
    ## @return path
    def ge_talgorithms_path(self):
        return self._algorithmspath

    ## Consulta o path da URL para acesso à dados de usuários
    ## @param self objeto
    ## @return path
    def get_users_path(self):
        return self._userspath

    ## Consulta o path da URL para acesso à dados de jobs
    ## @param self objeto
    ## @return path
    def get_jobs_path(self):
        return self._jobspath

    ## Consulta o path da URL para acesso ao pull de jobs
    ## @param self objeto
    ## @return path
    def get_jobs_pull_path(self):
        return self._jobspullpath

    ## Consulta o path da URL para acesso ao cancelamento de jobs
    ## @param self objeto
    ## @return path
    def get_jobs_cancel_path(self):
        return self._jobscancelpath

    ## Consulta a conexão corrente do objeto.
    ## @param self objeto
    ## @return conexão
    def get_connection(self):
        return self._connection

    ## Função utilitária de preenchimento
    def _fill_me(self, info, mefieldname, infofieldname, function):
        infofield = info.get(infofieldname)
        if infofield is None:
           self._me[mefieldname] = None
        else:
           self._me[mefieldname] = function(infofield)