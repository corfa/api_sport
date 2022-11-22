from sqlalchemy.orm import Session

from db.model.all_model import Employees, Abonnements


def create_employ(session: Session, name: str, phone_number: str, department_id: int, date_born: str) -> int:
    new_employ = Employees(

        full_name=name,
        phone_number=phone_number,
        department_id=department_id,
        date_born=date_born,

    )

    session.add(new_employ)
    session.commit()
    return new_employ.id


def get_employee_id_by_name(session: Session, name: str) -> int:
    return session.query(Employees.id).filter(Employees.full_name == name).first()[0]


def get_all_employees_on_id_deportament(session: Session, id: int):
    result = []
    employees = session.query(Employees).filter(Employees.department_id == id).all()
    for i in employees:
        result.append(
            {"full_name": i.full_name, "id": i.id, "department_id": i.department_id, "phone_number": i.phone_number,
             "abonnement_status": session.query(Abonnements).filter(Abonnements.employees_id == i.id).first().activ})

    return result
