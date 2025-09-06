# from fastapi import APIRouter
# from app.api.v1 import users, roles, products

# api_router = APIRouter()

# # 각 도메인의 router를 모아서 api_router에 등록
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
# api_router.include_router(products.router, prefix="/products", tags=["products"])