from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    def response(self):
        return {"code_transaction": self.default_code, "message": self.default_detail}


class TwilioServiceAPIException(BaseAPIException):
    status_code = 500
    default_code = "TWILIO_SERVICE_ERROR"

    def response(self):
        return {"code_transaction": self.default_code, "message": self.detail}
