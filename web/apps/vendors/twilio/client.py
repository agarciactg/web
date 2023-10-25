import logging

from django.conf import settings
from twilio.rest import Client

from web.apps.vendors.twilio.exceptions import TwilioServiceAPIException

logger = logging.getLogger(__name__)


class Twilio:
    """
    Service of Twilio
    """

    _ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
    _AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
    _PHONE_SENDER = settings.TWILIO_PHONE_SENDER

    def __init__(self) -> None:
        try:
            self.client = Client(self._ACCOUNT_SID, self._AUTH_TOKEN)
        except Exception as e:
            logger.exception(e)
            raise TwilioServiceAPIException("Error inicializando el cliente de Twilio")

    def send_sms(self, to: str, msg: str) -> bool:
        """
        Enviar sms
        :type to: str
        example +573001110022
        """
        try:
            message = self.client.messages.create(body=msg, from_=self._PHONE_SENDER, to=to)
            if message.status == "sent" or message.status == "queued":
                return True
            else:
                return False
        except Exception as e:
            logger.exception(e)
            raise TwilioServiceAPIException(str(e))

    def send_verify_code(self, phone: str) -> bool:
        """
        Enviar código de verificacion
        :type to: str
        example: +573001110022
        """
        try:
            code = ""
            message = f"web: Su código de verificación es {code}"
            send = self.send_sms(phone, message)
            if send:
                return True
            return send
        except Exception as e:
            raise TwilioServiceAPIException(str(e))
