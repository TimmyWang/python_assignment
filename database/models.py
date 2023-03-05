from sqlalchemy import Column, Integer, String, Date, Float, Index

from database import Base
from config.db import SYMBOL_MAX_LENGTH



class FinancialData(Base):  

    __tablename__ = "financial_data"
    
    id          = Column(Integer, primary_key=True, index=True)
    symbol      = Column(String(SYMBOL_MAX_LENGTH), nullable=False)
    date        = Column(Date, nullable=False, index=True)
    open_price  = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume      = Column(Integer, nullable=False)

    __table_args__ = (
        Index('idx_symbol_date', symbol, date),
    )

