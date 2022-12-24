from fastapi import FastAPI
from starlette.responses import FileResponse

from config.config_app import ConfigApp
from db.database import DataBase
from sqlalchemy import create_engine
from fastapi.responses import JSONResponse
from db.model.all_model import Base
from db.queries.aboniment_q import change_status_aboniment, create_aboniment
from db.queries.departament_q import get_departamet_id, get_all_departament
from db.queries.employees_q import get_all_employees_on_id_departaments, create_employ, get_data_employee_on_id, \
    delete_employee_on_id, change_employee
from db.queries.report_q import get_data_for_report_activ_abonnement_in_file, \
    get_data_for_report_noactiv_abonnement_in_file, get_data_for_report_noactiv_abonnement_on_departamet_in_file, \
    get_data_for_report_activ_abonnement_on_departamet_in_file
from db.queries.responsibles_q import verification_of_the_responsible, create_responsible, delete_responsible, \
    change_responsible



app = FastAPI()

config = ConfigApp()

engine = create_engine(
    config.url,
)
db = DataBase(engine)
session = db.make_session()




# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)




#EMPOYEE ENDPOINTS
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
async def read_item(id_employee: int):
    try:
        employee_id = delete_employee_on_id(session, id_employee)
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





@app.get("/get_all_employees_on_id_departaments/")
async def read_item(id_departaments: str):
    try:
        list_id = [int(i) for i in id_departaments.split(",")]
        all_employees = get_all_employees_on_id_departaments(session, list_id)
        return {"result": all_employees}
    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)



#ABONIMENT ENDPOINT
@app.get("/change_status_aboniment/")
async def read_item(id_employ: int):
    try:
        status = change_status_aboniment(session, id_employ)
        return {"result": status}
    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


#DEPARTAMENT ENDPOINT
@app.get("/get_all_departament")
async def report():
    try:
        departament = get_all_departament(session)
        return {"result": departament}

    except:
        return JSONResponse(content={"message": "something wrong"}, status_code=400)




#RESPONSIBLE ENDPOINTS

@app.get("/verification/")
async def read_item(name_responsible: str):
    try:
        responsible = verification_of_the_responsible(session, name_responsible)
        return {"result": responsible}

    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.post("/create_responsible")
async def read_item(last_name_responsible: str, id_departaments: str):
    try:
        list_id = [int(i) for i in id_departaments.split(",")]
        responsible = create_responsible(session, last_name_responsible, list_id)
        return {"result": responsible.id}
    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.delete("/delete_responsible")
async def read_item(id_responsible: int):
    try:
        delete_responsible(session, id_responsible)
        return {"result": id_responsible}
    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)


@app.patch("/change_responsible")
async def read_item(id_responsible: int, last_name: str, id_departaments: str):
    try:
        list_id = [int(i) for i in id_departaments.split(",")]
        change_responsible(session, id_responsible, last_name, list_id)

        return {"result": change_responsible}
    except:
        return JSONResponse(content={"message": "Invalid data"}, status_code=400)






#REPORT ENDPOINTS
@app.get("/get_report_activ_aboniment")
async def report():
    try:
        get_data_for_report_activ_abonnement_in_file(session)
        return FileResponse("report/отчёт по активным admin.xlsx", filename="отчёт по активным.xlsx", )
    except:
        return JSONResponse(content={"message": "something wrong"}, status_code=400)


@app.get("/get_report_noactiv_aboniment")
async def report():
    try:
        get_data_for_report_noactiv_abonnement_in_file(session)
        return FileResponse("report/отчёт по неактивным admin.xlsx", filename="отчёт по неактивным.xlsx", )
    except:
        return JSONResponse(content={"message": "something wrong"}, status_code=400)


@app.get("/get_report_noactiv_aboniment_in_departament")
async def read_item(id_departaments: str):
    try:
        list_id = [int(i) for i in id_departaments.split(",")]
        get_data_for_report_noactiv_abonnement_on_departamet_in_file(session, list_id)
        return FileResponse("report/отчёт по неактивным responsible.xlsx", filename="отчёт по неактивным.xlsx", )
    except:
        return JSONResponse(content={"message": "something wrong"}, status_code=400)


@app.get("/get_report_activ_aboniment_in_departament")
async def read_item(id_departaments: str):
    try:
        list_id = [int(i) for i in id_departaments.split(",")]
        get_data_for_report_activ_abonnement_on_departamet_in_file(session, list_id)
        return FileResponse("report/отчёт по активным responsible.xlsx", filename="отчёт по активным.xlsx", )
    except:
        return JSONResponse(content={"message": "something wrong"}, status_code=400)







# uvicorn main:app --reload
