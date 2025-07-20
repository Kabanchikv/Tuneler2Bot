from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    join_date = Column(DateTime, default=datetime.datetime.utcnow)
    subscriptions = relationship("Subscription", back_populates="user")

class Tariff(Base):
    __tablename__ = 'tariffs'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tariff_id = Column(Integer, ForeignKey('tariffs.id'), nullable=False)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    subdomain = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    payment_id = Column(String, nullable=True)
    
    user = relationship("User", back_populates="subscriptions")
    tariff = relationship("Tariff")