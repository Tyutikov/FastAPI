from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    Numeric,
    Date,
    text,
    Text
)
from src.db.database import Base

class Currency(Base):
    __tablename__ = "cbr_currency"

    id = Column(Text)
    num_code = Column(Integer)
    char_code = Column(String(3), primary_key=True)
    nominal = Column(Integer)
    name = Column(Text)
    value = Column(Numeric)
    v_unit_rate = Column(Numeric)
    cbr_date = Column(Date, primary_key=True)
    update_date = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
