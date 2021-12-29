from tortoise import Tortoise

from adapters.repositories.session.generic import AbstractSession
from settings import TORTOISE_ORM


class DBSession(AbstractSession):
    async def open(self) -> None:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()

    async def clean(self) -> None:
        connection = Tortoise.get_connection("default")
        await connection.execute_query(
            """
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                    EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
            """
        )

    async def start(self, transaction: any) -> None:
        await transaction.start()

    async def commit(self, transaction: any) -> None:
        await transaction.commit()

    async def rollback(self, transaction: any) -> None:
        await transaction.rollback()

    async def close(self) -> None:
        await Tortoise.close_connections()
