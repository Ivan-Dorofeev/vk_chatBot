"""
Функции, которая получает text (текст входящего сообщения) и context (dict) , возвращает bool:
True если шаг пройден, False если введено неверно.
"""
import datetime
import re

import dispatcher
from dispatcher import cities, is_city_in_dict
from make_fly_ticket.make_fly_ticket import make_ticket

re_name = re.compile(r'^[\w\-\s]{3,40}$')
re_email = re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b")
re_city = re.compile(r"^\w[a-zа-я]$")
re_date = re.compile(r"^\d{4}-\d{2}-\d{2}$")
re_yes = re.compile(r"(да)")
re_no = re.compile(r"(нет)")
re_phone_number = re.compile(r"\d{11}")


def handler_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handler_email(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['email'] = matches[0]
        return True
    else:
        return False


def handler_city_to(text, context):
    match = re.match(re_name, text)
    text = text.capitalize()
    if text in cities and is_city_in_dict(city=text):
        context['city_to'] = str(match[0]).capitalize()
        dispatcher.dict_to_dispather['step2'] = text
        return True
    else:
        c_list = ' \n'.join(list(cities[str(context['city_from']).capitalize()].keys()))
        context['city_to_list'] = c_list
        print(context)
        return False


def handler_city_from(text, context):
    match = re.match(re_name, text)
    text = text.capitalize()
    if text in cities and cities[text]:
        context['city_from'] = str(match[0]).capitalize()
        dispatcher.dict_to_dispather['step1'] = text
        return True
    else:
        return False


def handler_date(text, context):
    today = datetime.date.today()
    match = re.match(re_date, text)
    if match:
        context['date'] = match[0]
        input_date = datetime.date(year=int(text[0:4]), month=int(text[5:7]), day=int(text[8:10]))
        if input_date >= today:
            dispatcher.dict_to_dispather['step3'] = text
            start_dispatcher = dispatcher.dispatcher()
            context['choose_ways'] = start_dispatcher[1]
            context['dispatcher_res_list'] = start_dispatcher[0]
            return True
        else:
            return False
    else:
        return False


def handler_choose_from_1_to_5(text, context):
    if str(text).isdigit():
        if int(text) in range(1, 6):
            context['people_count'] = text
            return True
        else:
            return False
    else:
        return False


def handler_choose_from_ways(text, context):
    if str(text).isdigit():
        print('Длина dispatcher_res_list =  ', len(context['dispatcher_res_list']))
        if int(text) in range(1, len(context['dispatcher_res_list']) + 1):
            context['number_choose_ways'] = text
            dispatcher.dict_to_dispather['step4'] = context['dispatcher_res_list'][int(text) - 1]
            return True
        else:
            return False
    else:
        return False


def handler_yes_or_no(text, context):
    match_yes = re.match(re_yes, text)
    if match_yes:
        return True
    else:
        return False


def handler_phone_number(text, context):
    match = re.match(re_phone_number, str(text))
    if match:
        context['phone_number'] = match[0]
        return True
    else:
        return False


def handler_comment(text, context):
    context['comment'] = str(text)
    return True


def generate_ticket(text, context, user_id):
    print(context)
    return make_ticket(id=str(user_id), from_=context['city_from'], to=context['city_to'], date=context['date'])
