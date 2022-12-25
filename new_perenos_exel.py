import pandas as pd
from sqlalchemy import create_engine

from config.config_app import ConfigApp
from db.database import DataBase
from db.queries.aboniment_q import create_aboniment
from db.queries.departament_q import create_departament, get_departament_id
from db.queries.employees_q import create_employ, get_employee_id_by_name, get_id_employee_on_phone_number
from db.queries.responsibles_q import create_responsible


def sop(session, s: list):
    r = []
    for i in s:
        r.append(get_departament_id(session, i))
    return r


config = ConfigApp()

engine = create_engine(
    config.url,
)
db = DataBase(engine)
session = db.make_session()

data = pd.read_excel('data.xlsx')
set_dep=set(data["Отдел"])

for i in set_dep:
    create_departament(session, i)

set_responsibles=set(data["Ответственный за тренажерку в вашем отделе"])
dict_={}
for i in set_responsibles:
    for j in range(len(data["Ответственный за тренажерку в вашем отделе"])):
        if i ==  data["Ответственный за тренажерку в вашем отделе"][j]:
            if i not in dict_:
                dict_[i]=[]
            dict_[i].append(data["Отдел"][j])
for i in dict_:
    dict_[i]= set(dict_[i])
    dict_[i]=sop(session,dict_[i])
    create_responsible(session,i,dict_[i])


for i in range(len(data["ФИО"])):
    is_em=True
    id_ = get_departament_id(session, data["Отдел"][i])
    if data["Списание "][i]==1400:
        is_em=False
    create_employ(session, name=data["ФИО"][i], phone_number=data["Номер телефона"][i], department_id=id_,
                  date_born=data["Дата рождения"][i],is_employee=is_em)

for i in range(len(data["Абонемент действует с"])):

    create_aboniment(session, str(data["Абонемент действует с"][i]), int(data["Списание "][i]),
                     get_id_employee_on_phone_number(session, str(data["Номер телефона"][i])))
