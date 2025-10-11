from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app import crud,schemas
from app.database import get_db

router = APIRouter()

@router.post("/{user_id}",response_model=schemas.AccountResponse)
def create_account(user_id:int,account:schemas.AccountCreate,db:Session=Depends(get_db)):
    user = crud.get_user_by_id(db,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="Utilisateur introuvable")
    return crud.create_account(db,account,user_id)

@router.get("/user/{use_id}",response_model=list[schemas.AccountResponse])
def get_accounts_by_user(user_id:int,db:Session = Depends(get_db)):
    accounts = crud.get_accounts_by_user(db,user_id)
    return accounts

@router.get("/{account_id}",response_model=schemas.AccountResponse)
def get_account_by_id(account_id:int,db:Session = Depends(get_db)):
    account = crud.get_account_by_id(db,account_id)
    if not account:
        raise HTTPException(status_code=404,detail="Compte introuvable")
    return account

@router.delete("/{account_id}")
def delete_account(account_id:int,db:Session = Depends(get_db)):
    deleted = crud.delete_account(db,account_id)
    if not deleted:
        raise HTTPException(status_code=404,detail="Compte introuvable")
    return {"message" : "Compte supprimé avec succès"}