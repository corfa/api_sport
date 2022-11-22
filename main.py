from fastapi import FastAPI

from config.config_app import ConfigApp
from db.database import DataBase
from sqlalchemy import create_engine
from fastapi.responses import JSONResponse
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

@app.post("/create_employ")
async def read_item(full_name: str, phone_number: str, department_name: str, date_born):
    try:
        employ_id = create_employ(session, name=full_name, phone_number=phone_number,
                                  department_id=get_deportamet_id(session, department_name), date_born=date_born)

        create_aboniment(session, employ_id=employ_id)

        return JSONResponse(content={"id": employ_id}, status_code=200)
    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.get("/verification/")
async def read_item(name_responsible: str):
    try:
        responsible = verification_of_the_responsible(session, name_responsible)
        return {"result": responsible}

    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.get("/get_all_employees_on_id_deportament/")
async def read_item(id_deportament: int):
    try:
        all_employees = get_all_employees_on_id_deportament(session, int(id_deportament))
        return {"result": all_employees}
    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.get("/change_status_aboniment/")
async def read_item(id_employ: int):
    try:
        status = change_status_aboniment(session, id_employ)
        return {"result": status}
    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)
# uvicorn main:app --reload
