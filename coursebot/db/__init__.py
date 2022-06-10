from pathlib import Path

import asyncpg
from loguru import logger
from tortoise import Tortoise

__all__ = (
    "MODELS_DIR",
    "init_db",
    "models",
    "utils"
)

from coursebot.config.config import Database, config

MODELS_DIR = "coursebot.db.models"
path = Path(__file__).resolve().parent
print(path)
print(f"sqlite://{path}/db.sqlite")
async def init_db(db: Database = config.db):
    logger.debug(f"Initializing Database {db.database}[{db.host}]...")
    data = {
        # "db_url": db.postgres_url,
        # "db_url": "sqlite://db/db.sqlite",
        "db_url": f"sqlite://{path}/db.sqlite",
        "modules": {"models": [MODELS_DIR]},
    }
    try:
        await Tortoise.init(**data)
        await Tortoise.generate_schemas()
    except asyncpg.exceptions.ConnectionDoesNotExistError as e:
        logger.warning(e)
        logger.info("Creating a new database ...")
        await Tortoise.init(**data, _create_db=True)
        await Tortoise.generate_schemas()
        logger.success(f"New database {db.database} created")

    logger.debug(f"Database {db.database}[{db.host}] initialized")
