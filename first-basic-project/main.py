import zoneinfo
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from models import Customer, Transaction, Invoice, CustomerCreate, CustomerUpdate, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select 


app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return{"message" : "hello world"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time")
async def time():
    return {"time": datetime.now()}


@app.get("/time2/{iso_code}")
async def time2(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

# --------------------
# Customers
#---------------------


# Se crea una función de id, mientras no se tenga base de datos.
db_customers: list[Customer] = []


# Con customerCreate estamos recibiendo datos, sin id.
# Con response_model=Customer devolvemos el modelo Customer, con id.

# CREATE
@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump()) # Validamos los datos recibidos
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

# GET ALL
@app.get("/customers", response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

# GET BY ID
@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db:
        return customer_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

# DELETE
@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db:
        session.delete(customer_db)
        session.commit()
        return {"message": "Customer deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

# PATCH
@app.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
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







@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

