from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    def response(self):
        return {"code_transaction": self.default_code, "message": self.default_detail}


class AcademicGroupsDoesNotExistsAPIException(BaseAPIException):
    status_code = 404
    default_detail = "No Existe registro del Grupo Academico"
    default_code = "ACADEMIC_GROUPS_DOES_NOT_EXIST"


class AcademicGroupsAlreadyExistsException(BaseAPIException):
    status_code = 400
    default_detail = "Ya existe un Grupo academico con los datos ingresados"
    default_code = "ACADEMIC_GROUPS_ALREADY_EXIST"
