
from cspybase.services.core.exception import CsPyException
from cspybase.services.core.access import CsPyAccess
from cspybase.services.job import CsPyJob

## Classe que representa um acesso bem sucedido a um servidor.
class CsPyJobAccess(CsPyAccess):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)


    ## Consulta a lista de jobs em um determinado projeto
    ## @param self objeto do tipo acesso
    ## @param projectId id do projeto
    ## @return uma tupla com os jobs.
    def get_jobs(self, project_id):
        if project_id:
            info = { 'q': "projectId==\"{}\"".format(project_id)}
        else:
            info = {}
        jobs = self.get_connection().get(self.get_jobs_path(), info, True)
        joblist = []
        jobit = iter(jobs['jobs'])
        for job in jobit:
            if not job:
                print('error!')
            joblist.append(CsPyJob(self.get_connection(), job))
        return tuple(joblist)

    ## Consulta de um job
    ## @param self objeto do tipo acesso
    ## @param jobId id do projeto
    ## @return um job.
    def get_job(self, job_id):
        resp = self.get_connection().get(self.get_jobs_path() + '/' + job_id, {})
        return CsPyJob(self.get_connection(), resp)

    ## faz submit de um job
    ## @param self objeto do tipo access
    ## @param algorithm objeto do tipo algorithm
    ## @projectId string com o id do projeto onde o job deve ser guardado
    ## @info dicionario com os parametros de execução 
    def submit_job(self, algorithm_id, version_id, project_id, info):
        params = {
                "remoteCommand": {
                    'algorithmId':algorithm_id,
                    'projectId': project_id,
                    'versionId': version_id
                },
                "args": info['args'], # parametros do algoritimo
                "description": info['description'],
                "priority": info['priority'],
                "email": 
                    info['email']
                ,
                "emailOnTerminated": False,
                "candidateMachines": [ ],
                "numberOfJobs": 1
                }
        return self.get_connection().post(self.get_jobs_path(), params, isJsonContent=True)

    ## Faz o polling do job e retorna o estado do job além de usas informaçoes
    ## @param self objeto do tipo access
    ## @projectId string com o id do projeto onde o job deve ser guardado
    ## @jobid string com o id do job a ser consultado
    ## @date timestamp em segundos 
    ## returns: uma lista com 2 elementos: [0]: string com o estado do job ou False em caso de erro
    ##                                     [1]: resposta da requisição com as infos do job
    def pull_job(self, project_id, job_id, date = 0):
        info = {
            'projectId': project_id,
            'jobId': job_id,
            'date': date
        }
        resp = self.get_connection().get(self.get_jobs_pull_path(), info, True)
        if 'jobs' in resp:
            state = resp['jobs'][0]['state']
        else:
            state = False
        return state, resp

    ## Fica fazendo o pooling do job e só retorna quando o Job termina
    ## @projectId string com o id do projeto onde o job deve ser guardado
    ## @jobid string com o id do job a ser consultado
    ## @date timestamp em segundos
    ## @maxtimeouts numero max de timeouts antes de retornar [opcional]. obs 0 == sem limite de timeout
    ## returns True quando o job chega ao estado de finished, false caso tenha atingido o numero max de timeouts sem chegar em finished
    def wait_job(self, project_id, job_id, date, verbose = False, max_timeouts = None):
        info = {
            'projectId': project_id,
            'jobId': job_id,
            'date': date
        }
        state = ""
        lastState = state
        timeouts = 0
        while state != "FINISHED":
            resp = self.get_connection().get(self.get_jobs_pull_path(), info, True)
            info['date'] = resp['date']
            if 'jobs' not in resp:
                timeouts += 1
                if max_timeouts and max_timeouts < timeouts:
                    if verbose:
                        print('Max timeouts achieved, returning from "waitforjob"')
                    return False
                continue
            state = resp['jobs'][0]['state']
            if verbose and lastState != state:
                lastState = state
                print('Job {} state: {}'.format(job_id, state))

        return True
    
    ## Cancela os jobs recebidos por parametro
    ## @jobids lista de strings contendo o id dos jobs a serem cancelados
    def cancel_jobs(self, jobids):
        info = {
            'jobIds': jobids
        }
        try: # Só vai continuar no fluxo normal se receber 200
            self.get_connection().post(self.get_jobs_cancel_path(), info)
            return True
        except CsPyException as e:
            print(e)
            return False
