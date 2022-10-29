from fastapi import FastAPI

from config.config_app import ConfigApp
from db.database import DataBase
from sqlalchemy import create_engine

from db.model.all_model import Base
from db.queries.employees_q import get_all_employees_on_id_deportament
from db.queries.responsibles_q import verification_of_the_responsible

app = FastAPI()

config = ConfigApp()

engine = create_engine(
    config.url,
)
db = DataBase(engine)
session = db.make_session()


# #Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
@app.get("/get_all_employees")
async def get_all_employees():
    pass


@app.get("/verification/")
async def read_item(name_responsible: str):
    res = verification_of_the_responsible(session, name_responsible)
    return {"result": res}


@app.get("/get_all_employees_on_id_deportament/")
async def read_item(id_deportament: int):
    res = get_all_employees_on_id_deportament(session, int(id_deportament))
    return {"result": res}
