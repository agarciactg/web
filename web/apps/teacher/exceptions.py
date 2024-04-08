from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    def response(self):
        return {"code_transaction": self.default_code, "message": self.default_detail}


class TeacherDoesNotExistsAPIException(BaseAPIException):
    status_code = 404
    default_detail = "No Existe registro del Docente"
    default_code = "TEACHER_DOES_NOT_EXIST"


class TeacherAlreadyExistsException(BaseAPIException):
    status_code = 400
    default_detail = "Ya existe un docente con los datos ingresados"
    default_code = "TEACHER_ALREADY_EXIST"
