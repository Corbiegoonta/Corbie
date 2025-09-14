from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Asset(Base):
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)  # e.g., stock, bond, real estate
    asset_class = Column(String)  # e.g., equity, fixed income, alternative

    prices = relationship("PriceDaily", back_populates="asset")

class PriceDaily(Base):
    __tablename__ = 'price_daily'
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    asset = relationship("Asset", back_populates="prices")