import json
from channels import Group


class Ws(object):
    def send(self, group, action, data={}, namespace='api', scope='pub'):
        group = '{}.{}.{}'.format(namespace, scope, group)

        content = {}
        content['data'] = data
        content['action'] = action
        Group(group).send({'text': json.dumps(content)})
