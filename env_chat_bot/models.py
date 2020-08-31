from pony.orm import Database, Required, Json, select

from Settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserStates(db.Entity):
    """Состояние польхователя внутри сценария"""
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


class Registration(db.Entity):
    """Заявка на регистрацию"""
    name = Required(str)
    city_from = Required(str)
    city_to = Required(str)
    date = Required(str)


db.generate_mapping(create_tables=True)
