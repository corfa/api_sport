import pandas as pd
from sqlalchemy.orm import Session

from db.model.all_model import Employees, Abonnements

from db.queries.departament_q import get_departament_id, get_departamet_name_on_id


def get_data_for_report_noactiv_abonnement_on_departamet_in_file(session: Session, id: list[id]):
    names,  deportament = [], []
    for i in id:
        employees = session.query(Employees).filter(Employees.department_id == i).all()

        for employ in employees:
            abonnement = session.query(Abonnements).filter(Abonnements.employees_id == employ.id).first()

            if abonnement.activ == False:
                names.append(employ.full_name)
                deportament.append(get_departamet_name_on_id(session, employ.department_id))
    data = {"names": names,  "departament": deportament}
    create_file_for_responsible_noactiv(data, "responsible")


def get_data_for_report_activ_abonnement_on_departamet_in_file(session: Session, id: list[int]):
    names,deportament,= [], []
    for i in id:
        employees = session.query(Employees).filter(Employees.department_id == i).all()
        for employ in employees:
            abonnement = session.query(Abonnements).filter(Abonnements.employees_id == employ.id).first()

            if abonnement.activ:
                names.append(employ.full_name)
                deportament.append(get_departamet_name_on_id(session, employ.department_id))
    data_activ = {"names": names,"departament": deportament}
    create_file_for_responsible_activ(data_activ, "responsible")


def get_data_for_report_activ_abonnement_in_file(session: Session):
    employees = session.query(Employees).all()
    names, phone_number, deportament, date_born, is_employ, abonnements_status, abonnements_cost, abonnements_date_start = [], [], [], [], [], [], [], []

    for employ in employees:
        abonnement = session.query(Abonnements).filter(Abonnements.employees_id == employ.id).first()
        if abonnement is None:
            print(employ.id)
        if abonnement.activ and abonnement != None:
            abonnements_status.append("активен")
            abonnements_date_start.append(str(abonnement.date_create))
            abonnements_cost.append(abonnement.cost)
            names.append(employ.full_name)
            phone_number.append(employ.phone_number)
            deportament.append(get_departamet_name_on_id(session, employ.department_id))
            date_born.append(employ.date_born)
            if employ.is_employee:
                is_employ.append("Работник")
            else:
                is_employ.append("Родственник")
    data_activ = {"names": names, "phone_number": phone_number, "departament": deportament, "date_born": date_born,
                  "is_employ": is_employ, "abonnements_date_start": abonnements_date_start,
                  "abonnements_status": abonnements_status, "abonnements_cost": abonnements_cost}
    create_file_for_activ_exel(data_activ, "admin")


def get_data_for_report_noactiv_abonnement_in_file(session: Session):
    employees = session.query(Employees).all()
    names, phone_number, deportament, date_born, is_employ, abonnements_status, abonnements_cost, abonnements_date_cancel = [], [], [], [], [], [], [], []
    for employ in employees:
        abonnement = session.query(Abonnements).filter(Abonnements.employees_id == employ.id).first()

        if abonnement.activ == False:
            abonnements_status.append("не активен")
            abonnements_date_cancel.append(str(abonnement.update_at))
            abonnements_cost.append(abonnement.cost)
            names.append(employ.full_name)
            phone_number.append(employ.phone_number)
            deportament.append(get_departamet_name_on_id(session, employ.department_id))
            date_born.append(employ.date_born)
            if employ.is_employee:
                is_employ.append("Работник")
            else:
                is_employ.append("Родственник")
    data_activ = {"names": names, "phone_number": phone_number, "departament": deportament, "date_born": date_born,
                  "is_employ": is_employ, "abonnements_date_cancel": abonnements_date_cancel,
                  "abonnements_status": abonnements_status, "abonnements_cost": abonnements_cost}
    create_file_for_noactiv_exel(data_activ, "admin")


def create_file_for_activ_exel(data: dict, file_name: str):
    df = pd.DataFrame({'Имя': data["names"],
                       'Номер телефона': data["phone_number"],
                       'департамент': data["departament"],
                       'дата рождения': data["date_born"],
                       'работик/родственник': data["is_employ"],
                       'Абонемент действует с': data["abonnements_date_start"],
                       'статус абонемента': data["abonnements_status"],
                       'стоимость абонемента': data["abonnements_cost"]})
    df.to_excel('report/отчёт по активным ' + file_name + '.xlsx', sheet_name='отчёт', index=False)


def create_file_for_noactiv_exel(data: dict, file_name: str):
    df = pd.DataFrame({'Имя': data["names"],
                       'департамент': data["departament"],
                       'дата рождения': data["date_born"],
                       'работик/родственник': data["is_employ"],
                       'дата отмены': data["abonnements_date_cancel"],
                       'статус абонемента': data["abonnements_status"],
                       'стоимость абонемента': data["abonnements_cost"]})
    df.to_excel('report/отчёт по неактивным ' + file_name + '.xlsx', sheet_name='отчёт', index=False)


def create_file_for_responsible_noactiv(data:dict,file_name:str):
    df = pd.DataFrame({'Имя': data["names"],
                       'департамент': data["departament"],})
    df.to_excel('report/отчёт по неактивным ' + file_name + '.xlsx', sheet_name='отчёт', index=False)


def create_file_for_responsible_activ(data: dict, file_name: str):
    df = pd.DataFrame({'Имя': data["names"],
                       'департамент': data["departament"],})
    df.to_excel('report/отчёт по активным ' + file_name + '.xlsx', sheet_name='отчёт', index=False)
