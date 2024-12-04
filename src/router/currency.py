from datetime import date
from typing import List
from fastapi import (
    HTTPException,
    Depends,
    APIRouter
)
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from src.db import models, schemas
from src.db.database import get_db

router = APIRouter(
    prefix="/currency",
    tags=["currency"]
)

@router.get(
    "/Test",
    response_model=List[schemas.CbrCurrency])
def test_currency(db: Session = Depends(get_db)):
    currency = db.query(models.Currency).limit(10).all()
    return currency

@router.get(
    "/LastUpdate",
    response_model=schemas.LastUpdate
)
def get_last_update(db: Session = Depends(get_db)):
    last_update = db.query(func.max(models.Currency.update_date)).first()
    db.commit()
    if not last_update[0]:
        raise HTTPException(status_code=404, detail="Data not found")

    response_object = {
        "last_update": last_update[0].strftime("%Y-%m-%d %H:%M:%S.%f%z")
    }
    return response_object

@router.get(
    "/CurrencyCode",
    response_model=schemas.Currency
)
def get_currency_code(db: Session = Depends(get_db)):
    currency_code = (db.query(models.Currency.char_code.distinct(), models.Currency.name)
                     .order_by(models.Currency.char_code).all())
    db.commit()
    if not currency_code:
        raise HTTPException(status_code=404, detail="Data not found")

    response_object = {
        "currency": [{"code": code[0], "name": code[1]} for code in currency_code]
    }
    return response_object

@router.get(
    "/GetCurrencyValue/currency_code={currency_code}&date_from={date_from}&date_from={date_to}",
    response_model=schemas.CurrencyData
)
def get_currency_value(currency_code: str, date_from: date, date_to: date, db: Session = Depends(get_db)):
    print(f'date_from: {date_from} currency_code: {currency_code:}')
    currency_value = (db.query(models.Currency.char_code,
                              models.Currency.cbr_date,
                              models.Currency.value)
                      .filter(and_(models.Currency.char_code == currency_code, models.Currency.cbr_date.between(date_from, date_to)))
                      .order_by(models.Currency.cbr_date).all()
                      )
    db.commit()
    if not currency_value:
        raise HTTPException(status_code=404, detail="Data not found")

    response_object = {
        "currency_data": [{"code": value[0], "date": value[1], "value": value[2]} for value in currency_value]
    }
    return response_object

@router.get(
    "/Currency/date={dt}",
    response_model=List[schemas.CbrCurrency])
def get_currency_by_date(dt: date, db: Session = Depends(get_db)):
    currency = (db.query(models.Currency).filter(models.Currency.cbr_date == dt)
                .order_by(models.Currency.char_code).all())
    if not currency:
        raise HTTPException(status_code=404, detail="Data not found")
    return currency
