from cspybase.services.core.object import CsPyObject
from cspybase.services.user.user import CsPyUser
from cspybase.services.core.exception import CsPyException
from datetime import datetime
import re

## Classe que representa um Job.
class CsPyJob(CsPyObject):
    
    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    ## @param info dicionário informativo do algoritmo.
    def __init__(self, connection, info):
        super().__init__(connection)
        self._me = {}
        self._versions = ()
        self._update_me(info)

    ## Consulta o id do algoritmo utilizado no job.
    ## @param self objeto do tipo job.
    ## @return string com o id do algoritmo utilizado no Job.
    def get_algorithm_id(self):
        return self._me['algorithmId']

    ## Consulta o identificador do job.
    ## @param self objeto do tipo job.
    ## @return o id.
    def get_id(self):
        return self._me['jobId']

    ## Consulta o usuário owner do job.
    ## @param self objeto do tipo job.
    ## @return o usuário.
    def get_owner(self):
        return self._me['owner']

    ## Consulta o estado do job.
    ## @param self objeto do tipo job.
    ## @return o estado.
    def get_state(self):
        return self._me['state']
    
    ## Consulta a maquina em que o job foi executado.
    ## @param self objeto do tipo job.
    ## @return o nome da maquina.
    def get_execution_machine(self):
        return self._me['executionMachine']

    ## Retorna o timestamp de criação do job
    ## @param self objeto do tipo job.
    ## @return o timestamp.
    def get_submission_time(self):
        return self._me['submissionTime']

    ## Retorna o timestamp da ultima modificação do job
    ## @param self objeto do tipo job.
    ## @return o timestamp.
    def get_last_modified_time(self):
        return self._me['lastModifiedTime']

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info dicionário informativo
    def _update_me(self, info):
        if info is None:
           raise CsPyException("info for job cannot be none!")
        self._me['jobId'] = info['jobId']
        self._me['algorithmId'] = info['algorithmId']
        self._me['algorithmVersion'] = info['algorithmVersion']
        self._me['algorithmName'] = info['algorithmName']
        self._me['executionMachine'] = info['executionMachine']  
        self._me['state'] = info['state']
        dataRep = [ int(x) for x in re.split( '[:T.-]', info['lastModifiedTime']) ]
        data = datetime(*dataRep)
        self._me['lastModifiedTime'] = int(data.timestamp())
        dataRep = [ int(x) for x in re.split( '[:T.-]', info['submissionTime']) ]
        data = datetime(*dataRep)
        self._me['submissionTime'] = int(data.timestamp())
        cnn = self.get_connection()
        # a resposta de job não traz todas as infos do usuario
        userInfo = { 'owner': {'id':info['jobOwner'],'name': info['jobOwnerName'], 'login':''} }
        self._fill_me(userInfo, 'owner', 'owner', lambda infovalue: CsPyUser(cnn, infovalue))
        # self._fillme(info, 'version', 'Version', lambda infovalue: CsPyAlgorithmVersion(self, cnn, infovalue))
        # self._updateversions(info.get('versions'))
        

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        myid = self.get_id()
        algoId = self.get_algorithm_id()
        owner = self.get_owner()
        return "job: " + myid + " - algoritmId" + algoId + " (Owner: " + str(owner) + ") " + "state: " + self.get_state()

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()
