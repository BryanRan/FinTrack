from sqlalchemy.orm import Session
from app import models,schemas
from decimal import Decimal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto") #hashage du mot de passe

#USER
def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_user(db:Session,user:schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username = user.username,
        email = user.email,
        password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db:Session,email:str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db:Session,id:int):
    return db.query(models.User).filter(models.User.id == id).first()

#ACCOUNT
def generate_account_number(db:Session) ->str:
    last_account = (
        db.query(models.Account).order_by(models.Account.id.desc()).first()
    )
    
    if not last_account:
        return "0000000000000001"
    last_number = int(last_account.account_number)
    new_number = last_number + 1
    
    return str(new_number).zfill(16)

def create_account(db:Session,account:schemas.AccountCreate,user_id:int):
    account_number = generate_account_number(db)
    balance=account.balance if account.balance is not None else Decimal("0.00")
    db_account = models.Account(
        account_number = account_number,
        balance=balance,
        user_id=user_id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_accounts_by_user(db:Session,user_id:int)->list[models.Account]:
    return db.query(models.Account).filter(models.Account.user_id == user_id).all()

def get_account_by_id(db:Session,account_id:int)->models.Account:
    return db.query(models.Account).filter(models.Account.id==account_id).first()

def update_account_balance(db:Session, account_id:int, amount:Decimal):
    account = get_account_by_id(db,account_id)
    if account:
        account.balance += amount
        db.commit()
        db.refresh(account)
        return account
    return None
        
def delete_account(db:Session,account_id:int):
    account = get_account_by_id(db,account_id)
    if account:
        db.delete(account)
        db.commit()
        return True
    return False

#TRANSACTION
def create_transaction(db:Session,transaction:schemas.TransactionCreate):
    account = get_account_by_id(db,transaction.account_id)
    if not account:
        raise ValueError("Compte source introuvable")
    if transaction.type == "deposit":
        update_account_balance(db,account.id,transaction.amount)
    elif transaction.type == "withdraw":
        if transaction.amount > account.balance:
            raise ValueError("Solde insuffisant pour le retrait")
        update_account_balance(db,account.id,-transaction.amount)
    elif transaction.type == "transfer":
        if not transaction.related_account_id:
            raise ValueError("Compte cible requis pour un virement")
        target_account = get_account_by_id(db,transaction.related_account_id)
        if not target_account:
            raise ValueError("Compte cible introuvable")
        if account.balance < transaction.amount:
            raise ValueError("Solde insuffisant pour le virement")
        update_account_balance(db,account.id,-transaction.amount)
        update_account_balance(db,target_account.id,transaction.amount)
    else:
        raise ValueError("Type de transaction invalide")
    db_transaction = models.Transaction(
        type=transaction.type,
        amount = transaction.amount,
        account_id=transaction.account_id,
        related_account_id=transaction.related_account_id,
        description=transaction.description
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction

def get_transaction_by_id(db:Session,transaction_id:int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def get_transactions_by_account(db:Session,account_id:int):
    return db.query(models.Transaction).filter(models.Transaction.account_id == account_id).order_by(models.Transaction.date.desc()).all()

def get_all_transactions(db:Session):
    return db.query(models.Transaction).order_by(models.Transaction.date.desc()).all()

def delete_transaction(db:Session, transaction_id:int)->bool:
    transaction = get_transaction_by_id(db,transaction_id)
    if transaction:
        db.delete(transaction)
        db.commit()
        return True
    return False

