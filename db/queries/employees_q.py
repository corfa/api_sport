from sqlalchemy.orm import Session

from db.model.all_model import Employees, Abonnements
from db.queries.aboniment_q import get_aboniment_on_id_employee


def create_employ(session: Session, name: str, phone_number: str, department_id: int, date_born: str,
                  is_employee: bool = True) -> int:
    new_employ = Employees(

        full_name=name,
        phone_number=phone_number,
        department_id=department_id,
        date_born=date_born,
        is_employee=is_employee

    )

    session.add(new_employ)
    session.commit()
    return new_employ.id


def get_employee_id_by_name(session: Session, name: str) -> int:
    return session.query(Employees.id).filter(Employees.full_name == name).first()[0]


def get_data_employee_on_id(session: Session, id: int) -> Employees:
    return session.query(Employees).filter(Employees.id == id).first()


def get_all_employees_on_id_departaments(session: Session, id: list[int]):
    result = []
    for j in id:
        employees = session.query(Employees).filter(Employees.department_id == j).all()
        for i in employees:
            result.append(
                {"full_name": i.full_name, "id": i.id, "department_id": i.department_id, "phone_number": i.phone_number,
                 "is_employee": i.is_employee,
                 "abonnement_status": session.query(Abonnements).filter(
                     Abonnements.employees_id == i.id).first().activ})

    return result


def get_id_employee_on_phone_number(session: Session, phone: str):
    employee = session.query(Employees).filter(Employees.phone_number == phone).first()
    return employee.id


def delete_employee_on_id(session: Session, id: int):
    aboniment = get_aboniment_on_id_employee(session, id)
    session.delete(aboniment)
    employee = session.query(Employees).filter(Employees.id == id).first()
    session.delete(employee)
    session.commit()
    return employee.id


def change_employee(session: Session, id: int, full_name: str, phone_number: str, department_id: int, date_born: str,
                    is_employee: bool):
    employee = session.query(Employees).filter(Employees.id == id).first()
    employee.last_name = full_name
    employee.phone_number = phone_number
    employee.date_born = date_born
    employee.is_employee = is_employee
    employee.department_id = department_id
    session.commit()
    return employee.id

