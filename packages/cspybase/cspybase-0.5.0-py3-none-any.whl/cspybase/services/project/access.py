
from cspybase.services.core.access import CsPyAccess
from cspybase.services.project.project import CsPyProject


## Classe que representa um acesso bem sucedido a um servidor.
class CsPyProjectAccess(CsPyAccess):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)

    ## Consulta a lista de projetos disponíveis para este acesso
    ## @param self objeto do tipo acesso
    ## @return uma tupla com os projetos.
    def get_projects(self):
        prjs = self.get_connection().get(self.get_projects_path(), {})
        prjlist = []
        itprjs = iter(prjs)
        for prj in itprjs:
            prjlist.append(CsPyProject(self.get_connection(), prj))
        return tuple(prjlist)

    ## Cria um novo projeto
    ## @param self objeto do tipo acesso
    ## @param name nome do novo projeto a ser criado
    ## @param description descrição do novo projeto (opcional)
    ## @return o novo projeto criado
    def create_project(self, name, description = None):
        if description is None:
           description = name
        params = {'name': name, 'description': description}
        info = self.get_connection().post(self.get_projects_path(), params)
        return CsPyProject(self.get_connection(), info)

    ## Retorna um projeto com base em seu nome
    ## @param self objeto do tipo acesso
    ## @param name o nome a ser pesquisado
    ## @return o projeto ou None (caso este não seja encontrado)
    def get_project(self, name):
        prjs = self.get_projects()
        for prj in prjs:
            if prj.get_name() == name:
               return prj
        return None

    ## Retorna um projeto com base em seu nome
    ## @param self objeto do tipo acesso
    ## @param projectid o id a ser pesquisado
    ## @return o projeto ou None (caso este não seja encontrado)
    def get_project_by_id(self, projectid):
        prj = self.get_connection().get(self.get_projects_path() + '/' + projectid, {})
        print(prj)
        return prj

    ## Apaga um projeto com base em seu nome.
    ## @param self objeto do tipo acesso
    ## @param name o nome a ser apagado
    def delete_project(self, name):
        prj = self.get_project(name)
        if prj is not None:
           prjid = prj.get_id()
           self.get_connection().delete(self.get_projects_path() + "/" + prjid, {})

    ## Apaga um projeto com base em seu id.
    ## @param self objeto do tipo acesso
    ## @param id do projeto a ser apagado
    def delete_project_by_id(self, id):
        self.get_connection().delete(self.get_projects_path() + "/" + id, {})
    

