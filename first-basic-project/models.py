from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship

#---------------------------
# Plan
#---------------------------

class CustomerPlan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")

class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str | None = Field(default=None)
    customers: list["Customer"] = Relationship(back_populates="plans", link_model=CustomerPlan)



#---------------------------
# Customer
#---------------------------

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
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(back_populates="customers", link_model=CustomerPlan)
# La relación debe estar en la clase que tiene table=True, en este caso en Customer, y se debe usar el nombre de la clase entre comillas para evitar errores de referencia circular.

#---------------------------
# Transaction
#---------------------------

class TransactionBase(SQLModel):
    amount: int | None = Field(default=None)
    description: str | None =Field(default=None)

class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")
    pass

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id : int = Field(default=None, foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")
#---------------------------
# Invoice
#---------------------------

class InvoiceBase(SQLModel):
    customer: Customer = Field(default=None)
    transactions: list[Transaction] = Field(default=None)
    total: int = Field(default=None)

    # Metodo
    @property
    def total(self):
        return sum(transaction.amount for transaction in self.transactions)
    

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int | None = Field(default=None, primary_key=True)