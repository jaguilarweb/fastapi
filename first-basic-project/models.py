from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field

# Es requerido agregar el Field para que se cree en la base de datos.

class CustomerBase(SQLModel):
    name: str = Field(default=None) # Para crear un índice en la base de datos
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class Transaction(BaseModel):
    id: int
    amount: int # Mejor que usar el tipo float para evitar problemas de precisión
    description: str | None


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int 

    # Metodo
    @property
    def total(self):
        return sum(transaction.amount for transaction in self.transactions)