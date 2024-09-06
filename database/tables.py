from sqlalchemy import Table, MetaData, Column, BigInteger, String, DateTime, Integer
from datetime import datetime


metadata = MetaData()

users = Table(
    "users_reg",
    metadata,
    Column("user_id", BigInteger, primary_key=True, autoincrement=False),
    Column("full_name", String),
    Column("user_login", String),
    Column("refer_id", BigInteger),
    Column("count_refer", Integer, default=0),
    Column("chat_member_counter", Integer, default=0),
    Column('date_reg', DateTime, default=datetime.now)
)
