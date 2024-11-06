from sqlalchemy.orm import Session
from schemas.shemas_user import User, UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, document: str):
    return db.query(UserCreate).filter(UserCreate.document == document).first()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = pwd_context.hash(user.password)
    hashed_user = pwd_context.hash(user.email+user.document)
    db_user = UserCreate(
        user_id=hashed_user,
        email=user.email,
        password=fake_hashed_password,
        document=user.document,
        name=user.name,
        type_document=user.type_document,
        contact_user=user.contact_user,
        created_at=user.created_at
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

    