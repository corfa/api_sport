import pandas as pd
from sqlalchemy.orm import Session

from db.model.all_model import Employees, Abonnements

from db.queries.departament_q import get_departamet_id, get_departamet_name_on_id



def get_data_for_report_in_file(session: Session):
    employees = session.query(Employees).all()
    names = []
    phone_number = []
    deportament = []
    date_born = []
    is_employ = []
    abonnements_status = []
    abonnements_cost = []
    for employ in employees:
        abonnement = session.query(Abonnements).filter(Abonnements.employees_id == employ.id).first()
        abonnements_cost.append(abonnement.cost)
        if abonnements_status:
            abonnements_status.append("активен")
        else:
            abonnements_status.append("не активен")
        names.append(employ.full_name)
        phone_number.append(employ.phone_number)
        deportament.append(get_departamet_name_on_id(session, employ.department_id))
        date_born.append(employ.date_born)
        if employ.is_employee:
            is_employ.append("Работник")
        else:
            is_employ.append("Родственник")
    data={"names": names, "phone_number": phone_number, "departament": deportament, "date_born": date_born,
            "is_employ": is_employ, "abonnements_status": abonnements_status, "abonnements_cost": abonnements_cost}
    create_file_exel(data)



def create_file_exel(data:dict):
    df = pd.DataFrame({'Имя': data["names"],
                       'Номер телефона': data["phone_number"],
                       'департамент': data["departament"],
                       'дата рождения':data["date_born"],
                       'работик/родственник':data["is_employ"],
                       'статус абонемента':data["abonnements_status"],
                       'стоимость абонемента':data["abonnements_cost"]})
    df.to_excel('report/отчёт.xlsx', sheet_name='отчёт', index=False)