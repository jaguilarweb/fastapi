from fastapi import APIRouter, status, HTTPException

from models import Plan
from sqlmodel import select
from db import SessionDep

router = APIRouter()

@router.post("/plans", response_model=Plan, status_code= status.HTTP_201_CREATED, tags=["plans"])
async def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

@router.get("/plans", response_model=list[Plan], tags=["plans"])
async def get_plans(session: SessionDep):
    query = select(Plan)
    plans = session.exec(query).all()
    return plans