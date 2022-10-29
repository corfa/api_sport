from sqlalchemy.orm import Session

from db.model.all_model import Departments


def create_deportament(session: Session, name: str) -> Departments:
    new_deportament = Departments(

        departament_name=name,

    )

    session.add(new_deportament)
    session.commit()
    return new_deportament


def get_deportamet_id(session: Session, name: str) -> int:
     return session.query(Departments.id, ).filter(Departments.departament_name == name).first()



def get_all_deportament(session: Session):
    return session.query(Departments.departament_name).all()

