context = {'city_from': 'Рим', 'city_to': 'Балли', 'date': '2020-09-15',
           'choose_ways': '1 2020-09-18 08:00:00 \n2 2020-09-18 15:00:00 \n3 2020-09-23 08:00:00 \n4 2020-09-23 15:00:00 \n5 2020-09-28 08:00:00',
           'dispatcher_res_list': ['1 2020-09-18 08:00:00', '2 2020-09-18 15:00:00', '3 2020-09-23 08:00:00',
                                   '4 2020-09-23 15:00:00', '5 2020-09-28 08:00:00'], 'number_choose_ways': '5',
           'people_count': '3', 'comment': 'огоооооо', 'phone_number': '89651478111'}

import peewee

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
    Registration.get_or_create(
        id=user,
        data=str(context['dispatcher_res_list'][int(context['number_choose_ways']) - 1])[2::],
        people=int(context['people_count']),
        telephon=int(context['phone_number']),
        comment=str(context['comment']),
        in_city=str(context['city_to']),
        out_city=str(context['city_from']),
    )


wr_to_db(user=2602, context=context)
