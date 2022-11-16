# import sqlite3
#
# from sqlalchemy import create_engine
#
# from config.config_app import ConfigApp
# from db.database import DataBase
# from db.queries.aboniment_q import create_aboniment
# from db.queries.deportament_q import create_deportament, get_deportamet_id, get_all_deportament
# from db.queries.employees_q import create_employe, get_employee_id_by_name
# from db.queries.responsibles_q import create_responsible
#
# conn = sqlite3.connect(r'sport.db')
# cur = conn.cursor()
#
#
# config = ConfigApp()
#
# engine = create_engine(
#     config.url,
# )
# db=DataBase(engine)
# session=db.make_session()
#
#
# cur.execute("SELECT Отдел FROM october_activ")
# all_results = cur.fetchall()
# mass_dep=set()
# for i in all_results:
#     mass_dep.add(i[0])
#
# for i in mass_dep:
#     create_deportament(session,i)
#
#
#
#
#
# cur.execute("SELECT responsibles, Отдел FROM october_activ")
# mass =set()
# all = cur.fetchall()
# for i in all:
#
#     mass.add(i)
#
# for i in mass:
#     id_ = get_deportamet_id(session,i[1])[0]
#     create_responsible(session,i[0],id_)
#
#
#
#
#
# cur.execute("SELECT ФИО,Номер_телефона,Дата_рождения ,Отдел FROM october_activ")
# w=cur.fetchall()
# for i in w:
#     id_=get_deportamet_id(session,i[3])[0]
#     create_employe(session,name=i[0],phone_number=i[1],department_id=id_,date_born=i[2])
#
# cur.execute("SELECT ФИО,Абонемент_действует_с,cost FROM october_activ")
# q=cur.fetchall()
# for i in q:
#     create_aboniment(session,i[1],i[2],get_employee_id_by_name(session,i[0]))