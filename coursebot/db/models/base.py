import datetime
import typing

from aiogram.types import BufferedInputFile
from loguru import logger
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_queryset_creator, PydanticListModel


class Channel(models.Model):
    skin = fields.CharField(100, index=True)
    link = fields.CharField(100, index=True)


class Course(models.Model):
    title = fields.CharField(255)
    level = fields.CharField(25, description="Начальный, Средний, Продвинутый")
    registered_user = fields.ForeignKeyField("models.RegisteredUser")


class RegisteredUser(models.Model):
    user = fields.OneToOneField('models.User', related_name="registered_user")
    first_name = fields.CharField(255, index=True)
    last_name = fields.CharField(255, index=True)
    patronymic = fields.CharField(255, index=True)
    birthdate = fields.DatetimeField()
    phone = fields.CharField(255, index=True)
    email = fields.CharField(255)
    courses: fields.ReverseRelation[Course]


class User(models.Model):
    user_id = fields.BigIntField(index=True, unique=True)
    username = fields.CharField(32, unique=True, index=True, null=True)
    first_name = fields.CharField(255, null=True)
    last_name = fields.CharField(255, null=True)
    locale = fields.CharField(32, default="ru")
    registered_at = fields.DatetimeField(auto_now_add=True)
    registered_user: RegisteredUser

    @classmethod
    async def count_all(cls):
        return await cls.all().count()

    @classmethod
    async def count_new_today(cls) -> int:
        return await cls.filter(registered_at=datetime.date.today()).count()

    @classmethod
    async def export_users(cls,
                           _fields: tuple[str],
                           _to: typing.Literal["text", "txt", "json"]) -> BufferedInputFile | str:
        UserPydanticList = pydantic_queryset_creator(User, include=_fields)
        users: PydanticListModel = await UserPydanticList.from_queryset(User.all())
        if _to == "text":
            users_list = list(users.dict()["__root__"])
            user_value_list = list(map(lambda x: str(list(x.values())), users_list))
            result = "\n".join(user_value_list)
        elif _to == "txt":
            users_list = list(users.dict()["__root__"])
            user_value_list = list(map(lambda x: str(list(x.values())), users_list))
            user_txt = "\n".join(user_value_list)
            result = BufferedInputFile(bytes(user_txt, "utf-8"), filename="users.txt")
        else:
            # json.dumps(ensure_ascii=False, default=str)
            result = BufferedInputFile(bytes(users.json(ensure_ascii=False), "utf-8"),
                                       filename="users.json")
        return result
