from rest_framework import status
from rest_framework.exceptions import APIException


class GeneralError(APIException):
    """
    General exception that also displays a message back to the user.

    To use;

    from lib.exceptions import GeneralError

    # Examples
    raise GeneralError(message='Something happened', detail={'blah': [1,2,3]}, tip='try doing x instead')
    raise GeneralError(message='Invalid request, list_name not set', tip='Set list_name as a queryparam')
    raise GeneralError(
        message='Invalid request, invalid method',
        detail={'method': method},
        tip='Method specified needs to be one of the registered ones'
    )
    raise GeneralError(detail={'method': method}, template='invalid_method')
    raise GeneralError(detail={'missing_param': 'viewname'}, template='missing_param')
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    templates = {
        'invalid_method': {
            'message': 'Invalid request, invalid method',
            'tip': 'Method specified needs to be one of the registered ones'
        },
        'missing_param': {
            'message': 'Invalid request, all the required queryparams are not set',
            'tip': 'Set the correct parameters, example ?param=123, or &param=123'
        },
        'missing_data': {
            'message': 'Invalid request, we didnt find all required data (POST)',
            'tip': 'Make sure all data is available in the POST'
        }
    }

    def __init__(self, message=None, detail=None, tip=None, template=None):
        self.detail = {}

        if self.templates.get(template):
            self.detail = self.templates.get(template)

        if message:
            self.detail['message'] = message

        if detail:
            self.detail['detail'] = detail

        if tip:
            self.detail['tip'] = tip
