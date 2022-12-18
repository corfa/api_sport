from fastapi import FastAPI
from starlette.responses import FileResponse

from config.config_app import ConfigApp
from db.database import DataBase
from sqlalchemy import create_engine
from fastapi.responses import JSONResponse
from db.model.all_model import Base
from db.queries.aboniment_q import change_status_aboniment, create_aboniment
from db.queries.departament_q import get_departamet_id, get_all_departament
from db.queries.employees_q import get_all_employees_on_id_departament, create_employ, get_data_employee_on_id, \
    delete_employee_on_id, change_employee
from db.queries.report_q import get_data_for_report_in_file
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

@app.post("/create_employee/")
async def read_item(full_name: str, phone_number: str, department_id: int, date_born, date_start_aboniment: str,
                    is_employee: bool = True, ):
    try:
        employ_id = create_employ(session, name=full_name, phone_number=phone_number,
                                  department_id=department_id, date_born=date_born,
                                  is_employee=is_employee)
        if is_employee is True:
            cost = 900
        else:
            cost = 1400
        create_aboniment(session, date_create=date_start_aboniment, employ_id=employ_id, cost=cost)

        return JSONResponse(content={"id": employ_id}, status_code=200)
    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.patch("/change_employee/")
async def read_item(id: int, full_name: str, phone_number: str, department_id: int, date_born, is_employee: bool):
    try:
        employee_id = change_employee(session, id, full_name=full_name, phone_number=phone_number, date_born=date_born,
                                      is_employee=is_employee, department_id=department_id)
        return {"result": employee_id}

    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.delete("/delete_employee/")
async def read_item(id: int):
    try:
        employee_id = delete_employee_on_id(session, id)
        return {"result": employee_id}

    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.get("/get_employee/")
async def read_item(id: int):
    try:
        employee_data = get_data_employee_on_id(session, id)
        return {"result": employee_data}

    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.get("/get_report")
async def report():
    try:
        get_data_for_report_in_file(session)
        return FileResponse("report/отчёт.xlsx", filename="отчёт.xlsx", )
    except:
        return JSONResponse(content={"message": "something wrong"}, status_code=400)


@app.get("/verification/")
async def read_item(name_responsible: str):
    try:
        responsible = verification_of_the_responsible(session, name_responsible)
        return {"result": responsible}

    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.get("/get_all_employees_on_id_departament/")
async def read_item(id_departament: int):
    try:
        all_employees = get_all_employees_on_id_departament(session, int(id_departament))
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


@app.get("/get_all_departament")
async def report():
    try:
        departament = get_all_departament(session)
        return {"result": departament}

    except:
        return JSONResponse(content={"message": "something wrong"}, status_code=400)

# uvicorn main:app --reload
