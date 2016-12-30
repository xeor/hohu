import os


def api_version(request):
    return {'API_VERSION': os.environ.get('VERSION', '*unknown*')}
