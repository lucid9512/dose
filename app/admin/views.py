from sqladmin import ModelView
from wtforms import PasswordField, SelectField
from markupsafe import Markup
from sqlalchemy import select, delete

from app.models.user import User, Role, UserRole
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

# Argon2 + Bcrypt 둘 다 지원
hasher = PasswordHash([Argon2Hasher(), BcryptHasher()])

from sqladmin import ModelView
from wtforms import PasswordField, SelectField
from markupsafe import Markup
from sqlalchemy import select, delete

from app.models.user import User, Role, UserRole
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

# 비밀번호 해싱기 (argon2 + bcrypt 지원)
hasher = PasswordHash([Argon2Hasher(), BcryptHasher()])


class UserAdmin(ModelView, model=User):
    # 리스트 화면 표시 컬럼 (hashed_password는 아예 제외)
    column_list = [User.id, User.email, User.is_active]

    # 폼에서 hashed_password 제외
    form_excluded_columns = [User.hashed_password]

    # 모델 컬럼만 rules에 포함 (password는 모델에 없으므로 빼야 함)
    form_create_rules = ("email", "is_active", "role_id")
    form_edit_rules   = ("email", "is_active", "role_id")

    form_overrides = {
        "role_id": SelectField,  # role_id는 가상 단일 선택 필드
    }

    # 🚩 폼 정의 (가상 필드 추가)
    async def scaffold_form(self, rules=None):
        Form = await super().scaffold_form(rules)

        # 비밀번호 필드 (가상)
        if not hasattr(Form, "password"):
            Form.password = PasswordField("Password")

        # Role 필드 (가상)
        if not hasattr(Form, "role_id"):
            Form.role_id = SelectField("Role", coerce=int)

        # 🚩 Role 목록 채우기
        async with self.session_maker() as session:
            roles = (await session.execute(select(Role))).scalars().all()
        Form.role_id.kwargs["choices"] = [(r.id, r.name) for r in roles]

        return Form

    # 🚩 폼이 열릴 때 현재 Role 값 세팅
    async def on_form_prefill(self, form, model):
        if model and model.id:
            async with self.session_maker() as session:
                current = (
                    await session.execute(
                        select(UserRole.role_id).where(UserRole.user_id == model.id)
                    )
                ).scalar_one_or_none()
            if current:
                form.role_id.data = current

    # 🚩 저장 직전 비밀번호 & Role 처리
    async def on_model_change(self, data, model, is_created, request):
        # 🔑 비밀번호 처리
        password = data.get("password")  # dict에서 꺼내야 함

        if is_created:
            if not (password and password.strip()):
                raise ValueError("신규 생성 시 비밀번호는 필수입니다.")
            model.hashed_password = hasher.hash(password)
        else:
            if password and password.strip():
                model.hashed_password = hasher.hash(password)

        # 🔑 Role 처리 (단일 선택 강제)
        role_id = data.get("role_id")
        async with self.session_maker() as session:
            await session.execute(delete(UserRole).where(UserRole.user_id == model.id))
            if role_id:
                session.add(UserRole(user_id=model.id, role_id=int(role_id)))
            await session.commit()


    # 🚩 안내 문구 추가
    async def render_form(self, *args, **kwargs):
        form_html = await super().render_form(*args, **kwargs)
        notice = Markup('<p style="color:red;">* 비밀번호 입력 시에만 변경 됩니다.</p>')
        return notice + form_html


class RoleAdmin(ModelView, model=Role):
    column_list = [Role.id, Role.name, Role.descrition]

