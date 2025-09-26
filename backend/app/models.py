# Import et préparation

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

from .database import Base

# Création d'une table Utilisateur: User

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),unique=True,index=True,nullable=False)
    email = Column(String(120),unique=True,index=True,nullable=False)
    password = Column(String(255),nullable=False)
    created_at = Column(DateTime,default=lambda:datetime.now(timezone.utc))
    
    accounts = relationship("Account",back_populates="owner")
    
