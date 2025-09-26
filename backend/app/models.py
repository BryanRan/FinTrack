# Import et préparation

from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

from .database import Base

# Création d'une table Utilisateur: User

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    username = Column(String(50),unique=True,index=True,nullable=False)
    email = Column(String(120),unique=True,index=True,nullable=False)
    password = Column(String(255),nullable=False)
    created_at = Column(DateTime,default=lambda:datetime.now(timezone.utc))
    
    accounts = relationship("Account",back_populates="owner")
    
class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    account_number = Column(String(10),unique=True,index=True,nullable=False)
    balance = Column(Numeric(12,2),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    
    owner = relationship("User",back_populates="accounts")
    transactions = relationship("Transaction",back_populates="account")
    
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    type = Column(Enum("deposit","withdraw","transfer",name="transaction_type"),index=True,nullable=False)
    amount = Column(Numeric(12,2),nullable=False)
    date = Column(DateTime,default=lambda:datetime.now(timezone.utc))
    account_id = Column(Integer,ForeignKey("accounts.id"),nullable=False)
    description = Column(String(255),nullable=True)
    
    account = relationship("Account",back_populates="transactions")
    
    