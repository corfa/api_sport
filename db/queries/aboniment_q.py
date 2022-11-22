from sqlalchemy.orm import Session
from datetime import datetime
from db.model.all_model import Abonnements


def create_aboniment(session: Session, date_create: str = str(datetime.now().time()), cost: int = 0,
                     employ_id: int = None) -> Abonnements:
    new_aboniment = Abonnements(
        date_create=date_create,
        employees_id=employ_id,
        activ=True,
        cost=cost,

    )

    session.add(new_aboniment)
    session.commit()
    return new_aboniment


def change_status_aboniment(session: Session, employ_id: int):
    aboniment = session.query(Abonnements).filter(Abonnements.employees_id == employ_id).first()
    if aboniment.activ:
        aboniment.activ = False
    else:
        aboniment.activ = True
    session.add(aboniment)
    session.commit()
    return aboniment.activ
