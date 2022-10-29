from sqlalchemy.orm import Session

from db.model.all_model import Responsibles


def create_responsible(session: Session, name: str, deportament_id: int) -> Responsibles:
    new_responsible = Responsibles(

        full_name=name,
        responsible_for_the_department_id=deportament_id,

    )

    session.add(new_responsible)
    session.commit()
    return new_responsible


def verification_of_the_responsible(session: Session, name) -> Responsibles:
    return session.query(Responsibles).filter(Responsibles.full_name == name).first()

