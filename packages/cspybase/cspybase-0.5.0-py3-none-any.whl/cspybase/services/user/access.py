
## @package access
## Módulo responsável pelo acesso (já estabelecido por conexão) a um sistema CSBase

from cspybase.services.core.access import CsPyAccess
from cspybase.services.user.user import CsPyUser


## Classe que representa um acesso bem sucedido a um servidor.
class CsPyUserAccess(CsPyAccess):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)

    ## Consulta a lista de usuários do sistema
    ## @param self objeto do tipo acesso
    ## @return uma tupla com objeto do tipo usuário
    def get_users(self):
        users = self.get_connection().get(self.get_users_path(), {})
        userslist = []
        usersiter = iter(users)
        for user in usersiter:
            userslist.append(CsPyUser(self.get_connection(), user))
        return tuple(userslist)

    ## Retorna um usuário com base em seu id
    ## @param self objeto do tipo acesso
    ## @param userid o id a ser pesquisado
    ## @return o usuário ou None (caso este não seja encontrado)
    def get_user(self, userid):
        users = self.get_users()
        for usr in users:
            if usr.get_id() == userid:
                return usr
        return None

