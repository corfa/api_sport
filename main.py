from fastapi import FastAPI

from config.config_app import ConfigApp
from db.database import DataBase
from sqlalchemy import create_engine

from db.model.all_model import Base
from db.queries.aboniment_q import change_status_aboniment, create_aboniment
from db.queries.deportament_q import get_deportamet_id
from db.queries.employees_q import get_all_employees_on_id_deportament, create_employ
from db.queries.responsibles_q import verification_of_the_responsible

app = FastAPI()

config = ConfigApp()

engine = create_engine(
    config.url,
)
db = DataBase(engine)
session = db.make_session()


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
@app.get("/get_all_employees")
async def get_all_employees():
    pass


@app.post("/create_employ")
async def read_item(full_name: str, phone_number: str, department_name: str, date_born):
    employ_id = create_employ(session, name=full_name, phone_number=phone_number,
                              department_id=get_deportamet_id(session,department_name), date_born=date_born)
    create_aboniment(session, employ_id=employ_id)
    return employ_id


@app.get("/verification/")
async def read_item(name_responsible: str):
    res = verification_of_the_responsible(session, name_responsible)
    return {"result": res}


@app.get("/get_all_employees_on_id_deportament/")
async def read_item(id_deportament: int):
    res = get_all_employees_on_id_deportament(session, int(id_deportament))
    return {"result": res}


@app.get("/change_status_aboniment/")
async def read_item(id_employ: int):
    res = change_status_aboniment(session, id_employ)
    return {"result": res}
# uvicorn main:app --reload
