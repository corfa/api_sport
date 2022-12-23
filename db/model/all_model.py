import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, ForeignKey, BOOLEAN, ARRAY

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    update_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    def __repr__(self):
        return f'{self.__class__.__name__}'


class Departments(BaseModel):
    __tablename__ = 'departments'
    departament_name = Column(VARCHAR(50), unique=True)


class Employees(BaseModel):
    __tablename__ = 'employees'
    full_name = Column(VARCHAR(60), nullable=False)
    # last_name = Column(VARCHAR(20), nullable=False)
    # second_name = Column(VARCHAR(30), nullable=False)

    phone_number = Column(VARCHAR(30), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    date_born = Column(VARCHAR(60), nullable=False)
    is_employee = Column(BOOLEAN(), nullable=False)


class Abonnements(BaseModel):
    __tablename__ = 'abonnements'
    date_create = Column(VARCHAR(60), nullable=True)
    employees_id = Column(Integer, ForeignKey('employees.id'))
    activ = Column(BOOLEAN(), nullable=False)
    cost = Column(Integer, nullable=False)


class Responsibles(BaseModel):
    __tablename__ = 'responsibles'
    last_name = Column(VARCHAR(60), nullable=False)
    # last_name = Column(VARCHAR(20), nullable=False)
    # second_name = Column(VARCHAR(30), nullable=False)
    responsible_for_the_department_id = Column(ARRAY(Integer))
