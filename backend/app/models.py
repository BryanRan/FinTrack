# Import et préparation

from sqlalchemy import Integer, Numeric, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship,Mapped,mapped_column
from sqlalchemy.sql import func
from datetime import datetime,timezone

from .database import Base

# Création d'une table Utilisateur: User

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int]= mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    username = mapped_column(String(50),unique=True,index=True,nullable=False)
    email = mapped_column(String(120),unique=True,index=True,nullable=False)
    password = mapped_column(String(255),nullable=False)
    created_at = mapped_column(DateTime(timezone=True),server_default=func.now()) # délégation à la base plutôt qu'au serveur python
    
    accounts = relationship("Account",back_populates="owner",cascade="all, delete-orphan")
    
class Account(Base):
    __tablename__ = "accounts"
    
    id = mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    account_number = mapped_column(String(20),unique=True,index=True,nullable=False)
    balance = mapped_column(Numeric(12,2),nullable=False)
    user_id = mapped_column(Integer,ForeignKey("users.id"),nullable=False,ondelete="CASCADE",onupdate="CASCADE")
    created_at = mapped_column(DateTime(timezone=True),server_default=func.now())
    
    owner = relationship("User",back_populates="accounts")
    transactions = relationship("Transaction",back_populates="account",cascade="all, delete-orphan")
    
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    type = mapped_column(Enum("deposit","withdraw","transfer",name="transaction_type"),index=True,nullable=False)
    amount = mapped_column(Numeric(12,2),nullable=False)
    date = mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
    account_id = mapped_column(Integer,ForeignKey("accounts.id"),nullable=False,ondelete="CASCADE",onupdate="CASCADE")    
    related_account_id = mapped_column(Integer,ForeignKey("accounts.id"),nullable=True,ondelete="SET NULL",onupdate="CASCADE")
    description = mapped_column(String(255),nullable=True)
    
    account = relationship("Account",back_populates="transactions")
    
    