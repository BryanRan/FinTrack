from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/",response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db,user.email)
    if existing_user:
        raise HTTPException(status_code=400,detail="Email déjà utilisé")
    return crud.create_user(db,user)

@router.get('/{user_id}',response_model=schemas.UserResponse)
def get_user(user_id:int,db:Session = Depends(get_db)):
    user = crud.get_user_by_id(db,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="Utilisateur introuvable")
    return user

@router.get("/email/{email}",response_model=schemas.UserResponse)
def get_user_by_email(email:str,db:Session = Depends(get_db)):
    user = crud.get_user_by_email(db,email)
    if not user:
        raise HTTPException(status_code=404,detail="Utilisateur introuvable")
    return user