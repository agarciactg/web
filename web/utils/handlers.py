import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)

EMPTY_FIELDS = "EMPTY_FIELDS"
ERROR_SERVER = "ERROR_SERVER"
ERROR_AUTH = "ERROR_AUTH"
NOT_EXIST = "NOT_EXIST"


def web_api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        """
        if any(
            (
                type(exc) is None,
                type(exc) is None,
            )
        ):
            logger.warning(exc)
            response.data = exc.response()
        """

        if response.status_code == 400:
            logger.exception(exc, exc_info=exc)
            response.data = {"code_transaction": EMPTY_FIELDS, "message": response.data}

        elif response.status_code == 401 or response.status_code == 403:
            logger.warning(exc, exc_info=exc)
            response.data = {"code_transaction": ERROR_AUTH, "message": response.data}

        elif response.status_code == 404:
            logger.exception(exc, exc_info=exc)
            response.data = {"code_transaction": NOT_EXIST, "message": "Objeto no existe"}

        else:
            logger.exception(exc, exc_info=exc)
            response.data = {"code_transaction": ERROR_SERVER, "message": response.data}
    else:
        logger.exception(exc, exc_info=exc)
        response = {"code_transaction": ERROR_SERVER, "message": str(exc)}
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
