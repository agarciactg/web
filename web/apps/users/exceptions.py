from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    def response(self):
        return {"code_transaction": self.default_code, "message": self.default_detail}


class UserDoesNotExistsAPIException(BaseAPIException):
    status_code = 404
    default_detail = "No existe registro del usuario"
    default_code = "USER_DOES_NOT_EXIST"


class UserRequiredAPIException(BaseAPIException):
    status_code = 400
    default_detail = "El usuario es requerido"
    default_code = "USER_REQUIRED"


class StudentUnauthorizedAPIException(BaseAPIException):
    status_code = 401
    default_detail = "No tiene autorizacion"
    default_code = "STUDENT_UNAUTHORIZED"


class UserUnauthorizedAPIException(BaseAPIException):
    status_code = 401
    default_detail = "No tiene autorizacion"
    default_code = "USER_UNAUTHORIZED"


class UserAlreadyExistAPIException(BaseAPIException):
    status_code = 400
    default_detail = "Ya existe un usuario registrado con esta información."
    default_code = "USER_ALREADY_EXIST"
