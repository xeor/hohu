import re
import json

from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer


class ApiConsumer(JsonWebsocketConsumer):
    http_user = True

    def connection_groups(self, **kwargs):
        return ['api.broadcast']

    def connect(self, message, **kwargs):
        # FIXME: Add groups from user-profile
        self.message.channel_session['subscriptions'] = {}

    def receive(self, content, **kwargs):
        data = content.get('data', {})
        action = content.get('action', 'heartbeat')

        if action == 'subscribe':
            self.subscribe(data=data)
        elif action == 'unsubscribe':
            self.unsubscribe(data=data)
        elif action == 'heartbeat':
            self.heartbeat()
        elif action == 'ping':
            self.ping()
        elif action == 'debug':
            self.debug(content)
        else:
            self.invalid_action()

    def disconnect(self, message, **kwargs):
        pass

    def _get_group_name(self, group):
        if not re.match(r'^[a-z0-9_\.-]{1,64}', group):
            return None

        # namespaces are not in use yet.. Might be usefull later
        namespace = 'api'

        # scopes:
        #   pub: Free for everyone to subscribe
        #   priv: Collect group-name by some other means, cant be directly subscribed to
        #   user-${username}: Group-names as wanted, but pinned to user
        scope = 'pub'

        return '{}.{}.{}'.format(namespace, scope, group)

    def subscribe(self, data):
        group_name = self._get_group_name(data.get('group', ''))

        group_data = {
            'save': data.get('save') is True,
            'tag': data.get('tag', None),
            'unsubscribe_tag_first': data.get('unsubscribe_tag_first', False) is True
        }

        if group_data['unsubscribe_tag_first'] and group_data['tag']:
            self._unsubscribe_tag(group_data['tag'])

        self.message.channel_session.modified = True
        self.message.channel_session['subscriptions'][group_name] = group_data
        Group(group_name).add(self.message.reply_channel)

    def _remove_subscription(self, group):
        self.message.channel_session.modified = True
        del self.message.channel_session['subscriptions'][group]
        Group(group).discard(self.message.reply_channel)

    def _unsubscribe_tag(self, tag):
        if tag and re.match(r'^[a-z]{1,64}', tag):
            subscriptions = self.message.channel_session.get('subscriptions', {})
            tagged_groups = {k: v for k, v in subscriptions.iteritems() if v.get('tag') == tag}
            for subscription_name in tagged_groups.keys():
                self._remove_subscription(subscription_name)

    def unsubscribe(self, data):
        group = self._get_group_name()
        if group:
            self._remove_subscription(group)

        self._unsubscribe_tag(data.get('tag', None))

    def ping(self):
        self.message.reply_channel.send({'text': json.dumps({'action': 'pong', 'data': 1})})

    def heartbeat(self):
        # Reload group memberships..
        # http://channels.readthedocs.io/en/latest/asgi.html#persistence
        for group_name, group_data in self.message.channel_session.get('subscriptions', {}).iteritems():
            Group(group_name).discard(self.message.reply_channel)
            Group(group_name).add(self.message.reply_channel)

    def debug(self, content):
        channel_session = dict(self.message.channel_session)
        if channel_session.get('_auth_user_hash'):
            channel_session.pop('_auth_user_hash')
        if channel_session.get('_auth_user_backend'):
            channel_session.pop('_auth_user_backend')
        print('Got debug:')
        print('  content: ', content)
        print('  reply_channel: ', self.message.reply_channel)
        print('  channel_session: ', channel_session)
        print('  user: ', self.message.user)
        print()

        self.send({
            'action': 'debug',
            'data': {
                'content': content,
                'reply_channel': str(self.message.reply_channel),
                'channel_session': channel_session,
                'user': str(self.message.user)
            }
        })

    def invalid_action(self):
        self.message.reply_channel.send({'text': json.dumps({'action': 'pong', 'data': 'sup?'})})
