# app/cli.py
import typer
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import async_session_maker
from app.models.user import Role, User, UserRole
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher


cli = typer.Typer()
# Argon2 + Bcrypt 둘 다 지원 (fastapi-users 기본 설정과 일치)
hasher = PasswordHash([Argon2Hasher(), BcryptHasher()])

@cli.command()
def create_roles(names: list[str] = typer.Argument(..., help="생성할 Role 이름들")):
    """
    여러 Role 생성
    예: 
      poetry run python -m app.cli create-role admin manager user
    """
    async def _create():
        async with async_session_maker() as session:
            for role_name in names:
                result = await session.execute(select(Role).where(Role.name == role_name))
                existing = result.scalar_one_or_none()
                if existing:
                    print(f"Role '{role_name}' 이미 존재함")
                    continue

                role = Role(name=role_name)
                session.add(role)
                print(f"Role 생성됨: {role_name}")

            await session.commit()

    asyncio.run(_create())


@cli.command()
def create_user(
    email: str = typer.Argument(..., help="사용자 이메일"),
    password: str = typer.Argument(..., help="사용자 비밀번호"),
    role: str = typer.Argument(..., help="부여할 Role (하나만)")
):
    """
    새 User 생성 + Role 매핑
    사용 예:
      poetry run python -m app.cli create-user aa@aaa.co.kr pw admin
    """
    async def _create():
        async with async_session_maker() as session:
            # 유저 생성
            user = User(
                email=email,
                hashed_password=hasher.hash(password),  # bcrypt 해싱
                is_active=True,
            )
            session.add(user)
            await session.flush()  # user.id 확보

            # Role 확인 (없으면 자동 생성)
            result = await session.execute(select(Role).where(Role.name == role))
            role_obj = result.scalar_one_or_none()
            if not role_obj:
                print(f"Role '{role}' 이(가) 존재하지 않습니다. 먼저 create-role 명령어로 생성하세요.")
                await session.rollback()  # 트랜잭션 되돌리기
                return

            # 매핑
            user_role = UserRole(user_id=user.id, role_id=role_obj.id)
            session.add(user_role)

            await session.commit()
            print(f"User 생성됨: {email}, Role={role}")

    asyncio.run(_create())


if __name__ == "__main__":
    cli()