from rolepermissions.roles import AbstractUserRole

class Usuario(AbstractUserRole):
    available_permissions = {
        'permissao_usuario': True,
    }

class Unidade(AbstractUserRole):
    available_permissions = {
        'permissao_unidade': True,
    }