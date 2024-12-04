from pydantic import BaseModel
from datetime import datetime, date
from typing import List

class CbrCurrency(BaseModel):
    id: str
    num_code: int
    char_code: str
    nominal: int
    name: str
    value: float
    v_unit_rate: float
    cbr_date: date
    update_date: datetime

    class Config:
        orm_mode = True

class LastUpdate(BaseModel):
    last_update: datetime

    class Config:
        orm_mode = True

class CurrencyDict(BaseModel):
    code: str
    name: str

class Currency(BaseModel):
    currency: List[CurrencyDict]

    class Config:
        orm_mode = True

class CurrencyValue(BaseModel):
    code: str
    date: date
    value: float

class CurrencyData(BaseModel):
    currency_data: List[CurrencyValue]

    class Config:
        orm_mode = True
