from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from models import Customer, CustomerCreate, CustomerUpdate, CustomerPlan, Plan
from db import SessionDep


router = APIRouter()

# CREATE
@router.post("/customers", response_model=Customer, tags=["Customers"], status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump()) # Validamos los datos recibidos
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

# GET ALL
@router.get("/customers", response_model=list[Customer], tags=["Customers"])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

# GET BY ID
@router.get("/customers/{customer_id}", response_model=Customer, tags=["Customers"])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db:
        return customer_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

# DELETE
@router.delete("/customers/{customer_id}", tags=["Customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db:
        session.delete(customer_db)
        session.commit()
        return {"message": "Customer deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

# PATCH
@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def edit_customer(customer_id: int, customer_data: CustomerUpdate , session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
        )
    
    customer_data_dict = customer_data.model_dump(exclude_unset=True) # Obtenemos un diccionario con los campos que se recibieron
    customer_db.sqlmodel_update(customer_data_dict) # Actualizamos solo los campos que se recibieron
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db) # Actualiza valor en memoria
    return customer_db

@router.post("/customers/{customer_id}/plans/{plan_id}", status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def suscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
        )
    
    plan_db = session.get(Plan, plan_id)
    if not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan doesn't exist"
        )
    
    customer_plan_db = CustomerPlan(customer_id=customer_db.id, plan_id=plan_db.id)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db) # Actualiza valor en memoria
    return customer_plan_db

@router.get("/customers/{customer_id}/plans", response_model=list[Plan], tags=["Customers"])
async def get_customer_plans(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
        )
    
    return customer_db.plans