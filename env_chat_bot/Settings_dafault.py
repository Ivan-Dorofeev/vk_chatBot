# https://vk.com/public194790108

from dispatcher import cities_for_view

TOKEN = '7ae9ef5408cf6363bd93d2a09c53d613457585474308f3e820ce8f010f9defdf17a13154833e7c12f62f5'
GROUP_ID = 194790108

INTENTS = [
    {
        'name': 'Cпасибо',
        'token': ('спасиб', 'супер'),
        'scenario': None,
        'answer': 'Вам спасибо за ваше обращение :)'
    },
    {
        'name': 'ticket',
        'token': ('/ticket', 'ticket'),
        'scenario': 'ticket',
        'answer': None
    },
    {
        'name': 'help',
        'token': ('/help', 'help'),
        'answer': 'Чтобы закзать авиабилет на самолёт введите "/ticket" и следуйте инструкциям'
    }
]

SCENARIOS = {

    'ticket': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Введите город отправления',
                'failure_text': f'Во введенном городе ошибка. Возможные города \n{cities_for_view}',
                'handler': 'handler_city_from',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите город назначения',
                'failure_text': 'Из города {city_from} возможны вылеты только в следующие города: \n '
                                ' {city_to_list} \n Введите нужный город:',
                'handler': 'handler_city_to',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Введите дату желаемого вылета в формате 2020-12-31',
                'failure_text': 'Формат даты следующий = 2020-12-31. Введите дату в верном формате.',
                'handler': 'handler_date',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Выберите понравившийся рейс: {choose_ways} ',
                'failure_text': 'Выберите один из вариантов (цифра)',
                'handler': 'handler_choose_from_ways',
                'next_step': 'step5'
            },
            'step5': {
                'text': 'На сколько пассажиров бронируем место? (от 1 до 5)',
                'failure_text': 'Количество мест от 1 до 5. Введите верное число',
                'handler': 'handler_choose_from_1_to_5',
                'next_step': 'step6'
            },
            'step6': {
                'text': ' Предлагаем написать комментарий в произвольной форме.',
                'failure_text': None,
                'handler': 'handler_comment',
                'next_step': 'step7'
            },
            'step7': {
                'text': 'Уточняем введенные данные. Пользователь должен ввести "да" или "нет". Если пользователь '
                        'вводит "нет", сценарий завершается с предложением попробовать еще раз.',
                'failure_text': 'Введите "да" (если согласны с введёнными данными), либо "нет" '
                                '(если не согласны и хотите начать снова)',
                'handler': 'handler_yes_or_no',
                'next_step': 'step8'
            },
            'step8': {
                'text': 'Запрашиваем номер телефона',
                'failure_text': 'Введите телефон в формате 89876543210',
                'handler': 'handler_phone_number',
                'next_step': 'step9'
            },
            'step9': {
                'text': 'Спасибо за Ваш заказ. Желаете пройти регистрацию снова? ',
                'failure_text': 'Всего доброго',
                'handler': 'handler_yes_or_no',
                'next_step': 'step1',

            }
        }
    }
}

DEFAULT_ANSWER = 'Не знаю как на это ответить. ' \
                 'Я могу зарегистрировать Вас на рейс. Напишите "/ticket" \n'

DB_CONFIG = dict(
    provider='postgres',
    user='',
    password='',
    host='',
    database='vk_chat_bot',
)
