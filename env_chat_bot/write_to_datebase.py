import peewee
from dispatcher import dict_to_dispather, dispatcher
from make_fly_ticket.make_fly_ticket import make_ticket

db = peewee.SqliteDatabase('registration.db')


class BassTable(peewee.Model):
    class Meta:
        database = db


class Registration(BassTable):
    """Создадим базу данных"""
    id = peewee.TextField()
    data = peewee.TextField()
    people = peewee.IntegerField()
    telephon = peewee.IntegerField()
    comment = peewee.TextField()
    in_city = peewee.TextField()
    out_city = peewee.TextField()


db.create_tables([Registration])


def wr_to_db(user, context):
    print('Пишем в Базу данных')
    print('context ', context['number_choose_ways'])
    print('context ', context['dispatcher_res_list'])
    print('context ', type(context['dispatcher_res_list']))
    a = int(context['number_choose_ways']) - 1
    print('data', context['dispatcher_res_list'][a])
    card_ticket = make_ticket(fio=user, from_=str(context['city_from']), to=str(context['city_to']),
                date=str(context['dispatcher_res_list'][int(context['number_choose_ways']) - 1])[2::])
    Registration.get_or_create(
        id=user,
        data=str(context['dispatcher_res_list'][int(context['number_choose_ways']) - 1])[2::],
        people=int(context['people_count']),
        telephon=int(context['phone_number']),
        comment=str(context['comment']),
        in_city=str(context['city_to']),
        out_city=str(context['city_from']),
    )

    return card_ticket
