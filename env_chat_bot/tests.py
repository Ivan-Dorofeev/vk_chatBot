from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock

from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotEvent, VkBotMessageEvent

import Settings
from vk_bot import Bot
from make_fly_ticket.make_fly_ticket import make_ticket


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session():
            test_func(*args, **kwargs)
            rollback()

    return wrapper


class Test1(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {'message': {'date': 1598594715, 'from_id': 5732771, 'id': 2382, 'out': 0,
                               'peer_id': 5732771, 'text': 'dwd',
                               'conversation_message_id': 2319, 'fwd_messages': [],
                               'important': False,
                               'random_id': 0, 'attachments': [], 'is_hidden': False},
                   'client_info': {'button_actions':
                                       ['text', 'vkpay', 'open_app', 'location', 'open_link'],
                                   'keyboard': True, 'inline_keyboard': True, 'carousel': False,
                                   'lang_id': 0}},

        'group_id': 183721469}

    INPUTS = [
        'привет',
        "спасиб",
        "/ticket",
        "Рим",
        "Токио",
        "Монтекарло",
        "2020-10-10",

    ]

    EXPECTED_OUTPUTS = [
        Settings.DEFAULT_ANSWER,
        Settings.INTENTS[0]['answer'],
        Settings.SCENARIOS['ticket']['steps']['step1']['text'],
        Settings.SCENARIOS['ticket']['steps']['step2']['text'],
        Settings.SCENARIOS['ticket']['steps']['step3']['text'],
    ]

    def test_run(self):
        count = 5
        obj = {'a': 1}
        event = [obj] * count
        long_poller_mock = Mock(return_value=event)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('vk_bot.vk_api.VkApi'):
            with patch('vk_bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    def test_on_event(self):
        pass

    @isolate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock
        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)
        with patch('vk_bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()
        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        count = 0
        for call in send_mock.call_args_list:
            count += 1
            args, kwargs = call
            real_outputs.append(kwargs['message'])
            if count == 5:
                break
        assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        with open("make_fly_ticket/51351351.png", 'rb') as avatar_file:
            avatar_mock = Mock()
            avatar_mock.content = avatar_file.read()
        with patch('requests.get', return_value=avatar_mock):
            ticket_file = make_ticket(id='51351351', from_='Paris', to='Madrid', date='2020-09-15')
        with open("make_fly_ticket/ticket_end.png", 'rb') as expected_file:
            assert ticket_file.read() == expected_file.read()
