import logging
import random
from datetime import datetime

from django.core.mail import mail_managers
from djmoney.money import Money as DjangoMoney

logger = logging.getLogger(__name__)


class Money(DjangoMoney):
    def __init__(self, *args, **kwargs):
        kwargs["currency"] = "COP"
        kwargs["decimal_places"] = 0
        kwargs["format_options"] = {
            "format": u"$#,##0",
            "currency_digits": False,
        }

        super().__init__(*args, **kwargs)


def generate_sms_code():
    return "".join(random.choice("123456789") for _ in list(range(4)))


def seconds_any_day(date):
    date_now = datetime.now()
    diff = date - date_now
    return diff.seconds + diff.days * 86400


def notify_admin_email(subject, message):
    mail_managers(subject, message)
