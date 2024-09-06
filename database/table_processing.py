from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy import insert, select

from database.tables import users as users_table


# функция, для получения информации по конкретному пользователю
async def get_user_data(user_id: int, db_engine: AsyncEngine) -> dict | None:
    stmt = (select("*").where(users_table.c.user_id == user_id))
    async with db_engine.connect() as conn:
        result = await conn.execute(stmt)
        user_data = result.fetchone()
        if user_data is not None:
            return dict(
                user_id=user_data[0],
                full_name=user_data[1],
                user_login=user_data[2],
                refer_id=user_data[3],
                count_refer=user_data[4],
                chat_member_counter=user_data[5],
                date_reg=user_data[6]
            )
    return user_data


# функция, для получения всех пользователей (для админки)
async def get_all_users_data(db_engine: AsyncEngine, count_refer_from_adm: int = 0):
    stmt = (
        select(
            users_table.c.user_id,
            users_table.c.full_name,
            users_table.c.user_login,
            users_table.c.refer_id,
            users_table.c.count_refer,
            users_table.c.chat_member_counter,
            users_table.c.date_reg
        )
        .where(users_table.c.count_refer >= count_refer_from_adm)
    )
    async with db_engine.connect() as conn:
        result = await conn.execute(stmt)
        users: list[dict] = [dict(row._mapping) for row in result]
    return users


# функция, для добавления пользователя в базу данных
async def insert_user(user_data: dict, db_engine: AsyncEngine) -> None:
    stmt = insert(users_table).values(
            user_id=user_data['user_id'],
            full_name=user_data['full_name'],
            user_login=user_data['user_login'],
            refer_id=user_data['refer_id'],
            count_refer=user_data['count_refer'],
            chat_member_counter=user_data['chat_member_counter']
        )
    async with db_engine.connect() as conn:
        await conn.execute(stmt)
        await conn.commit()


# функция, для изменения счетчика количества каналов на которые подписан
async def change_chat_member_counter(user_id: int, db_engine: AsyncEngine, plus: bool = True) -> None:
    stmt = (
            users_table.update()
            .where(users_table.c.user_id == user_id)
            .values(
                chat_member_counter=(users_table.c.chat_member_counter + 1)
                if plus
                else (users_table.c.chat_member_counter - 1))
        )
    async with db_engine.connect() as conn:
        await conn.execute(stmt)
        await conn.commit()


# функция, для изменения счетчика количества приведенных рефералов
async def change_count_refer(refer_id: int, db_engine: AsyncEngine, plus: bool = True) -> None:
    stmt = (
            users_table.update()
            .where(users_table.c.user_id == refer_id)
            .values(
                count_refer=(users_table.c.count_refer + 1)
                if plus
                else (users_table.c.count_refer - 1))
        )
    async with db_engine.connect() as conn:
        await conn.execute(stmt)
        await conn.commit()
