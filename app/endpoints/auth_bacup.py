# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.ext.asyncio import AsyncSession
# from ..database import get_db
# from ..dao.models_dao import UserDAO
# from ..auth import verify_password, create_access_token
#
# router = APIRouter(prefix="/auth", tags=["authentication"])
#
# @router.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
#     user = await UserDAO.get_by_username(db, form_data.username)
#     if not user or not verify_password(form_data.password, user.password_hash):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}