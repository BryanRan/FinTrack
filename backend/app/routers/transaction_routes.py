from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app import crud,schemas
from app.database import get_db

router = APIRouter()
@router.post("/",response_model=schemas.TransactionResponse)
def create_transaction(transaction:schemas.TransactionCreate,db:Session = Depends(get_db)):
    try:
        return crud.create_transaction(db,transaction)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@router.get("/{transaction_id}",response_model=schemas.TransactionResponse)
def get_transaction(transaction_id:int,db:Session = Depends(get_db)):
    transaction = crud.get_transaction_by_id(db,transaction_id)
    if not transaction:
        raise HTTPException(status_code=404,detail="Transaction introuvable")
    return transaction

@router.get("/account/{account_id}",response_model=list[schemas.TransactionResponse])
def get_transaction_by_acount(account_id:int,db:Session = Depends(get_db)):
    return crud.get_transactions_by_account(db,account_id)

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id:int,db:Session = Depends(get_db)):
    deleted = crud.delete_transaction(db,transaction_id)
    if not deleted:
        raise HTTPException(status_code=404,detail="Transaction introuvable")
    return {"message" : "Transaction supprimée avec succès"}