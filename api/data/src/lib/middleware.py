import os


class SetBaseEnv(object):
    """
    Figure out which port we are on if we are running and set it.

    So that the links will be correct.
    Not sure if we need this always...
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if os.environ.get('HTTP_PORT') and ':' not in request.META['HTTP_HOST']:
            request.META['HTTP_HOST'] = '{}:{}'.format(request.META['HTTP_HOST'], os.environ['HTTP_PORT'])

        response = self.get_response(request)
        return response
