import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from models import  Transaction, Invoice, Transaction, Invoice
from db import create_all_tables
from .routers import customers


app = FastAPI(lifespan=create_all_tables)
# Incluimos el router de customers en la aplicación principal
app.include_router(customers.router) 

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



@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

