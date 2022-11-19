from sqlalchemy.orm import Session

from db.model.all_model import Employees


def create_employ(session: Session, name: str, phone_number: str, department_id: int, date_born: str) -> Employees:
    new_employ = Employees(

        full_name=name,
        phone_number=phone_number,
        department_id=department_id,
        date_born=date_born,

    )

    session.add(new_employ)
    session.commit()
    return new_employ


def get_employee_id_by_name(session: Session, name: str) -> int:
    return session.query(Employees.id).filter(Employees.full_name == name).first()[0]


def get_all_employees_on_id_deportament(session: Session, id: int):
    return session.query(Employees).filter(Employees.department_id == id).all()
