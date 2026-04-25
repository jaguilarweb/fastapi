import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from models import Customer, Transaction, Invoice, CustomerCreate, Transaction, Invoice

app = FastAPI()

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

# Se cre un afunción de id, mientras no se tenga base de datos.
db_customers: list[Customer] = []


# Con customerCreate estamos recibiendo datos, sin id.
# Con response_model=Customer devolvemos el modelo Customer, con id.
@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate):
    customer = Customer.model_validate(customer_data.model_dump()) # Validamos los datos recibidos
    # Asumiendo que lo hace la base de datos (fake).
    customer.id = len(db_customers)
    db_customers.append(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def list_customers():
    return db_customers

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

