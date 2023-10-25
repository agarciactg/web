import json


def process_response(response):
    """
    Processes test api response.
    :param response:
    :return: (result, code_transaction, data, message)
    """
    result = json.loads(response.content.decode("utf8"))
    code_transaction = result.get("code_transaction")
    message = result.get("message", None)
    data = result.get("data", None)

    return result, code_transaction, data, message
