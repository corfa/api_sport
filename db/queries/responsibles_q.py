from sqlalchemy.orm import Session

from db.model.all_model import Responsibles


def create_responsible(session: Session, name: str, deportament_id: list) -> Responsibles:
    new_responsible = Responsibles(

        last_name=name,
        responsible_for_the_department_id=deportament_id,

    )

    session.add(new_responsible)
    session.commit()
    return new_responsible


def verification_of_the_responsible(session: Session, name) -> Responsibles:
    return session.query(Responsibles).filter(Responsibles.last_name == name).first()


def delete_responsible(session: Session, id: int)->int:
    responsible = session.query(Responsibles).filter(Responsibles.id == id).first()
    session.delete(responsible)
    session.commit()
    return responsible.id


def change_responsible(session: Session, id: int, last_name: str, department_id: list[int]):
    responsible = session.query(Responsibles).filter(Responsibles.id == id).first()
    responsible.last_name=last_name
    responsible.responsible_for_the_department_id=department_id
    session.commit()
    return responsible.id