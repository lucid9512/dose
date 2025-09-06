from fastapi import FastAPI
from sqladmin import Admin
from app.core.db import engine
from .views import UserAdmin, RoleAdmin

def init_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(RoleAdmin)
            
    return admin
