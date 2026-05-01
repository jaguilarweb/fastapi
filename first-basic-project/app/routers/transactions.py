from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
# Importar el modelo de transacción
from models import Customer, Transaction, TransactionCreate, TransactionUpdate
from db import SessionDep


router = APIRouter()


# CREATE
@router.post("/transactions", response_model=Transaction, tags=["Transactions"], status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    # Proceso de validación de los datos mediante pydant
    transaction_data_dic= transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dic["customer_id"]) # Validamos que el customer_id exista en la base de datos
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    transaction_db=Transaction.model_validate(transaction_data_dic)
    # Conección con la base de datos.
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

# GET ALL
@router.get("/transactions", response_model=list[Transaction], tags=["Transactions"], status_code=status.HTTP_200_OK)
async def list_transactions(session: SessionDep):
    return session.exec(select(Transaction)).all()


# GET BY ID
@router.get("/transactions/{transaction_id}", response_model=Transaction, tags=["Transactions"], status_code=status.HTTP_200_OK)
async def read_transaction(transaction_id: int, session: SessionDep):
    # Código
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction_db

# PATCH

# DELETE




