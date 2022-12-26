from sqlalchemy.orm import Session

from db.model.all_model import Departments
from db.queries.employees_q import get_all_employees_on_id_departaments, delete_employee_on_id


def create_departament(session: Session, name: str) -> Departments:
    new_deportament = Departments(

        departament_name=name,

    )

    session.add(new_deportament)
    session.commit()
    return new_deportament


def get_departament_id(session: Session, name: str) -> int:
    return session.query(Departments).filter(Departments.departament_name == name).first().id


def get_departamet_name_on_id(session: Session, id: int) -> str:
    if session.query(Departments.departament_name, ).filter(Departments.id == id).first() is None:
        return ""
    return session.query(Departments.departament_name, ).filter(Departments.id == id).first()[0]


def get_all_departament(session: Session):
    return session.query(Departments.id, Departments.departament_name).all()


def change_departament(session: Session, id: int, name_departament: str):
    departament = session.query(Departments).filter(Departments.id == id).first()
    departament.departament_name = name_departament
    session.commit()
    return departament.id


def del_departament(session: Session, id: int):
    employess = get_all_employees_on_id_departaments(session, [id])
    for employee in employess:
        delete_employee_on_id(session, employee["id"])
    departament = session.query(Departments).filter(Departments.id == id).first()
    session.delete(departament)
    session.commit()
    return departament.id
