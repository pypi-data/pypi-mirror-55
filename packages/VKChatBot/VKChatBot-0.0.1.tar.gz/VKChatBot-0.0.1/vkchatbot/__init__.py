import requests
from typing import Callable, Union, Optional
from .objects import SendableMessage


def get_session_requests():
    session = requests.Session()
    session.headers['Accept'] = 'application/json'
    session.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    return session


class VKChatBot:
    def __init__(self, access_token, group_id, api_url='https://api.vk.com/method/', v='5.80',
                 command_prefix='!'):
        self.access_token = access_token
        self.group_id = group_id
        self.api_url = api_url
        self.api_version = v
        self._session = get_session_requests()
        self._prefix = command_prefix
        self._commands = {}
        self.unknown_command_msg = 'Unknown command. Type %shelp to see list of commnands' % command_prefix

    def unknown_command_handler(self, event) -> Optional[Union[str, SendableMessage]]:
        return self.unknown_command_msg

    def _poll_events(self):
        poll = self._session.get(url=f'{self.api_url}groups.getLongPollServer', params={
            'group_id': self.group_id,
            'access_token': self.access_token,
            'v': self.api_version
        }).json()['response']
        server, key, ts = poll['server'], poll['key'], poll['ts']
        while True:
            long_poll = self._session.post(server, data={
                'act': 'a_check',
                'key': key,
                'ts': ts,
                'wait': 25,
            }).json()
            for update in long_poll['updates']:
                yield update
            ts = long_poll['ts']

    def register_command(self, command: str, handler: Callable):
        self._commands[command] = handler

    def unregister_command(self, command: str):
        del self._commands[command]

    def _process_command(self, event):
        text = event['object']['text']
        if not text.startswith(self._prefix):
            return
        cmd = text.lower().split()[0][len(self._prefix):]
        handler = self._commands.get(cmd, self.unknown_command_handler)
        return handler(event)

    def send_message(self, peer_id, message: Union[str, SendableMessage]):
        if isinstance(message, str):
            params = {'message': message}
        else:
            params = message.to_dict()
        self._session.post(f'{self.api_url}messages.send', data={
            'peer_id': peer_id,
            'access_token': self.access_token,
            'v': self.api_version,
            **params,
        })

    def work(self):
        for event in self._poll_events():
            if event['type'] == 'message_new':
                result = self._process_command(event)
                if result is not None:
                    peer_id = event['object']['peer_id']
                    self.send_message(peer_id, result)


__all__ = ['VKChatBot', 'objects']
