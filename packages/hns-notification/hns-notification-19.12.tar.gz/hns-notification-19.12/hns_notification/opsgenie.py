import opsgenie_sdk


def configure(api_key, url=None):
    """
    Configures opsgenie api parameters
    :param api_key: Opsgenie api key
    :type api_key: str
    :param url: URL/Host of the opsgenie API. By default it is 'https://api.opsgenie.com'. You shouldn't need to
    change it
    :type url: str
    :return: Opsgenie API client object
    :rtype: object
    """

    conf = opsgenie_sdk.Configuration()
    conf.api_key['Authorization'] = api_key
    if url is not None:
        conf.host = url
    return opsgenie_sdk.ApiClient(conf)


def create_alert(api_client, alert_body):
    """
    Creates and sends opsgenie alert
    :param api_client: Opsgenie api client object
    :type api_client: object
    :param alert_body: Alert body fields. Check https://docs.opsgenie.com/docs/python-sdk-alert#section-create-alert
    for details on accepted alert body field
    :type alert_body: dict
    :return: Opsgenie response object
    :rtype: object
    """

    body = opsgenie_sdk.CreateAlertPayload(**alert_body)
    alert_api = opsgenie_sdk.AlertApi(api_client)
    response = alert_api.create_alert(body)
    return response

