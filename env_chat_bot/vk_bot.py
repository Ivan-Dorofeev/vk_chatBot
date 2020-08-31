import logging
import random

import requests
from pony.orm import db_session

from env_chat_bot import Settings_local
import handlers
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from models import UserStates, Registration

try:
    import Settings
except ImportError:
    exit('DO COPY Settings.py and set token')

log = logging.getLogger('Bot')


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter(fmt='%(levelname)s - %(message)s', datefmt="%d %m %Y %H:%M"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s - %(message)s'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)


class Bot:
    """
    Echo Bot for vk.com
    Use Python 3.7
    """

    def __init__(self, token, group_id):
        """
        :param token: секретный токен
        :param group_id: группа id из группы в vk.com
        """
        self.token = token
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(vk=self.vk, group_id=self.group_id)
        self.api = self.vk.get_api()
        self.user_states = dict()  # user_id -> UserState

    def run(self):
        """Запуск Бота"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('ошибка в обработке события')
                # raise ValueError('Неизвестное сообщение')

    @db_session
    def on_event(self, event):
        """
        Обрабатывает собщение Бота.
        Отправляет сообщение назад, если сообщение текст
        """

        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info("Не умеем обрабатывать такое событие такого типа %s", event.type)
            return
        user_id = event.message.peer_id
        text = event.message.text
        text_to_send = ''
        state = UserStates.get(user_id=str(user_id))

        if state is not None:
            self.continue_scenario(text, state, user_id)
        else:
            for intent in Settings.INTENTS:
                log.debug(f'User gets {intent}')
                if any(token in text.lower() for token in intent['token']):
                    if intent['answer']:
                        self.send_text(intent['answer'], user_id)
                    else:
                        self.start_scenario(user_id, intent['scenario'], text)
                    break
            else:
                self.send_text(Settings.DEFAULT_ANSWER, user_id)

    def send_text(self, text_to_send, user_id):
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id
        )

    def send_image(self, image, user_id):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_data = requests.post(url=upload_url, files={'photo': ('image.png', image, 'image/png')}).json()
        image_data = self.api.photos.saveMessagesPhoto(**upload_data)
        owner_id = image_data[0]['owner_id']
        media_id = image_data[0]['id']
        attachment = f'photo{owner_id}_{media_id}'

        self.api.messages.send(
            attachment=attachment,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id
        )

    def send_step(self, step, user_id, text, context):
        if 'text' in step:
            self.send_text(step['text'].format(**context), user_id)
        if 'image' in step:
            handler = getattr(handlers, step['image'])
            image = handler(text, context, user_id)
            self.send_image(image, user_id)

    def start_scenario(self, user_id, scenario_name, text):
        scenario = Settings.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        self.send_step(step, user_id, text, context={})
        UserStates(user_id=str(user_id), scenario_name=scenario_name, step_name=first_step, context={})

    def continue_scenario(self, text, state, user_id):
        steps = Settings.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            # next step
            next_step = steps[step['next_step']]
            self.send_step(next_step, user_id, text, state.context)

            if next_step['next_step']:
                # swith to next steps
                state.step_name = step['next_step']
            else:
                # finish scenario
                Registration(name=str(user_id),
                             city_from=state.context['city_from'],
                             city_to=state.context['city_to'],
                             date=state.context['date'])
                # del from psql
                state.delete()
        else:
            text_to_send = step['failure_text'].format(**state.context)
            self.send_text(text_to_send, user_id)


if __name__ == '__main__':
    configure_logging()
    bot = Bot(token=Settings_local.py.TOKEN, group_id=Settings_local.GROUP_ID)
    bot.run()

# Серия вопросиков:
# 1) Для запуска скрипта из 16-го задания, мы скрип пишет только в самом терминале PyCharm. Через терминал ОС он не
#  работает, т.к. не видит импорты. Чтобы он работал через терминал ОС, нам нужно убрать импорты всё в один файл внести?
# ODO Импорты надо строить относительно одной рабочей директории, в которой находится главный запускаемый модуль
# ODO Далее нужно каким-нибудь образом выбрать рабочую директорию
# ODO в терминале она пряму в строке указана и её можно менять через команду cd переходя из папки в папку
# ODO просто в пайчарме можно зайти в run/edit configuration и там это настроить
# 3) Всё, что клиент вводит нужно в базу данных записать, верно?)
# ODO да, сперва в UserState, а затем из UserState всё удалить, когда регистрация будет завершена
# ODO и сделать запись в таблице с регистрациями.
# ODO Чтобы по итогу были данные о регистрации и была возможность у пользователя начать сценарий с 0
