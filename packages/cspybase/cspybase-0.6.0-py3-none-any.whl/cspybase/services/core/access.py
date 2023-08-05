## @package access
## Módulo responsável pelo acesso (já estabelecido por conexão) a um sistema CSBase
from cspybase.services.core.exception import CsPyUnconnectedException
from cspybase.services.core.object import CsPyObject


## Classe que representa um acesso bem sucedido a um servidor.
class CsPyAccess(CsPyObject):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)

