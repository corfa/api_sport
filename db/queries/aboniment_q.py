from datetime import datetime, date, time
from sqlalchemy.orm import Session
from db.model.all_model import Abonnements


def create_aboniment(session: Session, date_create: str, cost: int,
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
    aboniment.update_at=change_date(datetime.now())
    session.add(aboniment)
    session.commit()
    return aboniment.activ


def get_aboniment_on_id_employee(session: Session, employ_id: int):
    return session.query(Abonnements).filter(Abonnements.employees_id == employ_id).first()


def change_date(date_):
    t = time(00, 00)
    if date_.month == 12:
        year = date_.year
        year += 1
        return datetime.combine(date(year, 1, 1), t)
    month = date_.month
    print(month)
    month += 1
    return datetime.combine(date(date_.year, month, 1), t)
