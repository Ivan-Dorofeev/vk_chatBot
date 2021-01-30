import re
from datetime import time, date

dict_to_dispather = {}

cities = {'Москва': {'Лондон': {'day': [1, 3, 10, 15, 20, 25, 30], 'times': [(10, 00), (20, 00)]},
                     'Париж': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(10, 00), (20, 00)]},
                     'Токио': {'day': [3, 7, 12, 17, 22, 27], 'times': [(10, 00), (20, 00)]},
                     'Рим': {'day': [4, 8, 13, 18, 23, 28], 'times': [(10, 00), (20, 00)]},
                     },
          'Лондон': {'Москва': {'day': [1, 4, 10, 15, 20, 25, 30], 'times': [(11, 00), (21, 00)]},
                     'Хельсинки': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(11, 00), (21, 00)]},
                     'Вашингтон': {'day': [3, 7, 12, 17, 22, 27], 'times': [(11, 00), (21, 00)]},
                     'Балли': {'day': [4, 8, 13, 18, 23, 28], 'times': [(11, 00), (21, 00)]},
                     'Сан-Антонио': {'day': [1, 5, 10, 20, 28], 'times': [(11, 00), (21, 00)]},
                     },
          'Париж': {'Вашингтон': {'day': [1, 5, 10, 15, 20, 25, 30], 'times': [(12, 00), (22, 00)]},
                    'Балли': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(12, 00), (22, 00)]},
                    'Токио': {'day': [3, 7, 12, 17, 22, 27], 'times': [(12, 00), (22, 00)]},
                    'Рим': {'day': [4, 8, 13, 18, 23, 28], 'times': [(12, 00), (22, 00)]},
                    },
          'Токио': {'Хельсинки': {'day': [1, 6, 11, 16, 21, 26, 29], 'times': [(9, 00), (19, 00)]},
                    'Москва': {'day': [3, 7, 12, 17, 22, 27], 'times': [(9, 00), (19, 00)]},
                    'Сан-Антонио': {'day': [4, 8, 13, 18, 23, 28], 'times': [(9, 00), (19, 00)]},
                    },
          'Рим': {'Лондон': {'day': [2, 5, 10, 15, 20, 25, 30], 'times': [(8, 00), (15, 00)]},
                  'Вашингтон': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(10, 00), (15, 00)]},
                  'Токио': {'day': [3, 7, 12, 17, 22, 27], 'times': [(8, 00), (15, 00)]},
                  'Балли': {'day': [4, 8, 13, 18, 23, 28], 'times': [(8, 00), (15, 00)]},
                  'Сан-Антонио': {'day': [1, 5, 10, 20, 28], 'times': [(8, 00), (15, 00)]}
                  },
          'Сан-Антонио': {'Лондон': {'day': [3, 5, 10, 15, 20, 25, 30], 'times': [(7, 00), (14, 00)]},
                          'Вашингтон': {'day': [2, 6, 11, 16, 21, 26, 29],
                                        'times': [(7, 00, 00), (14, 00)]},
                          'Балли': {'day': [4, 8, 13, 18, 23, 28], 'times': [(7, 00), (14, 00)]},
                          'Рим': {'day': [1, 5, 10, 20, 28], 'times': [(7, 00), (14, 00)]},
                          'Хельсинки': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(7, 00), (14, 00)]}
                          },
          'Хельсинки': {'Лондон': {'day': [2, 5, 10, 15, 20, 25, 30], 'times': [(10, 00), (12, 00)]},
                        'Вашингтон': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(7, 00), (16, 00)]},
                        'Балли': {'day': [4, 8, 13, 18, 23, 28], 'times': [(10, 00), (12, 00)]},
                        'Рим': {'day': [1, 5, 10, 20, 28], 'times': [(7, 00), (16, 00)]},
                        'Москва': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(5, 00), (12, 00)]}
                        },
          'Вашингтон': {'Лондон': {'day': [1, 7, 10, 15, 20, 25, 30], 'times': [(13, 00), (18, 00)]},
                        'Париж': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(7, 00), (18, 00)]},
                        'Балли': {'day': [4, 8, 13, 18, 23, 28], 'times': [(10, 00), (18, 00)]},
                        'Сан-Антонио': {'day': [1, 5, 10, 20, 28], 'times': [(7, 00), (18, 00)]},
                        'Москва': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(5, 00), (18, 00)]}
                        },
          'Балли': {'Рим': {'day': [1, 6, 10, 15, 20, 25, 30], 'times': [(13, 00), (18, 00)]},
                    'Париж': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(7, 00), (18, 00)]},
                    'Лондон': {'day': [4, 8, 13, 18, 23, 28], 'times': [(10, 00), (18, 00)]},
                    'Сан-Антонио': {'day': [1, 5, 10, 20, 28], 'times': [(7, 00), (18, 00)]},
                    'Москва': {'day': [2, 6, 11, 16, 21, 26, 29], 'times': [(5, 00), (18, 00)]}
                    }}

today = date.today()
today_day = date.today().day
re_date = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def dispatcher():
    # ODO Вместо глобальных переменных - попробуйте возвращать данные из функции через return
    # ODO Тогда можно будет явно использовать необходимые данные в нужных местах
    print(dict_to_dispather)
    city_out = str(dict_to_dispather['step1']).capitalize()
    city_in = str(dict_to_dispather['step2']).capitalize()
    date_in = dict_to_dispather['step3']
    all_dates_for_cities = {}
    res = []
    for search_city in cities.keys():
        if city_out == search_city:
            for days in cities[city_out][city_in]['day']:
                all_dates_for_cities[days] = cities[city_out][city_in]['times']
            need_date = int(date_in[-2:])
            need_month = int(date_in[-5:-3])
            result_list = {}
            for keys in all_dates_for_cities.keys():
                if int(keys) > need_date:
                    result_list[keys] = all_dates_for_cities[keys]
            limit = 0
            for dates, times in result_list.items():
                for hours in range(0, len(times)):
                    limit += 1
                    if limit > 5:
                        break
                    res.append(
                        f'{limit} {date(year=today.year, month=need_month, day=dates)}'
                        f' {time(hour=int(times[hours][0]), minute=int(times[hours][1]))}')
    print('res', res)
    result_times = ' \n'.join(res)
    print("Готов список вылетов: ", result_times)
    return res, result_times


cities_for_view = ' \n'.join(list(cities))


def view_choose_city():
    first_city = str(dict_to_dispather['step1']).capitalize()
    print('first_city = ', first_city)
    return first_city


def view_chooses():
    first_city = view_choose_city()
    view_city_chooses = '\n'.join(cities[str(first_city)].keys())
    print('second_city = ', view_city_chooses)
    return view_city_chooses


def is_city_in_dict(city):
    our_city = view_choose_city()
    city_in = str(city)
    if city_in in cities[str(our_city)].keys():
        return True
    else:
        return False
