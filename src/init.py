import asyncio
from sqlalchemy.future import select

from src.database.session import get_standalone_session
from src.models import Role


async def fill_roles():

    async with get_standalone_session() as session:
        roles = [
            Role(name="SuperAdmin"),
            Role(name="Admin"),
            Role(name="Chef"),
            Role(name="Manager"),
        ]
        q = await session.execute(select(Role))
        ex_roles = q.scalars().all()
        for role in roles:
            if role.name in [r.name for r in ex_roles]:
                continue
            session.add(role)
            await session.commit()
            await session.refresh(role)


def init():
    asyncio.create_task(fill_roles())
