from sqlalchemy.orm import Session

from db.model.all_model import Departments


def create_departament(session: Session, name: str) -> Departments:
    new_deportament = Departments(

        departament_name=name,

    )

    session.add(new_deportament)
    session.commit()
    return new_deportament


def get_departamet_id(session: Session, name: str) -> int:
    return session.query(Departments ).filter(Departments.departament_name == name).first().id


def get_departamet_name_on_id(session: Session, id: int) -> str:
    if session.query(Departments.departament_name, ).filter(Departments.id == id).first() is None:
        return ""
    return session.query(Departments.departament_name, ).filter(Departments.id == id).first()[0]



def get_all_departament(session: Session):
    return session.query(Departments.id,Departments.departament_name).all()
