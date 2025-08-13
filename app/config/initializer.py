from typing import Any, Optional, Union

from sqlalchemy import URL, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from app.config.config import DATABASE_URL

Base = declarative_base()


class Initializer:

    def __init__(self) -> None:
        self.SessionLocal: Optional[sessionmaker[Session]] = None
        self.SessionLocalAsync: Optional[Any] = None  # Type for async sessionmaker

    def connect_to_db(self) -> None:
        if not self.SessionLocal:
            engine = create_engine(
                str(DATABASE_URL),
                echo=False,
                poolclass=QueuePool,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=10,
            )
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
            )
        self._test_db_connection()

    async def connect_to_db_async(self) -> None:
        if not self.SessionLocalAsync:
            async_engine = create_async_engine(
                str(DATABASE_URL),
                echo=False,
                poolclass=QueuePool,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=10,
            )
            # Use async_sessionmaker for async sessions
            from sqlalchemy.ext.asyncio import async_sessionmaker

            self.SessionLocalAsync = async_sessionmaker(
                async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )
        await self._test_db_connection_async()

    def _test_db_connection(self) -> bool:
        if self.SessionLocal is None:
            return False
        session = self.SessionLocal()
        try:
            session.execute(text("SELECT 1"))
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
        finally:
            session.close()
        return True

    async def _test_db_connection_async(self) -> bool:
        if self.SessionLocalAsync is None:
            return False
        try:
            async with self.SessionLocalAsync() as session:
                await session.execute(text("SELECT 1"))
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
        finally:
            await session.close()
        return True
