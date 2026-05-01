from sqlmodel import Session

from db import engine
from models import Transaction, Customer

session = Session(engine)
customer = Customer(
    name="John Doe",
    description="A regular customer",
    email="jon@midomain.com",
    age=30
)
session.add(customer)
session.commit()

for x in range(100):
    session.add(
        Transaction(
            customer_id=customer.id,
            description=f"Transaction {x}",
            amount=10 * x,
        )
    )
session.commit()

