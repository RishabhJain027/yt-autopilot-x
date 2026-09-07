import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from packages.config.settings import settings
from database.schema import Base

os.makedirs(settings.STORAGE_ROOT, exist_ok=True)
for sub in ['raw', 'research', 'audio', 'captions', 'scenes', 'renders', 'thumbnails', 'uploads', 'published', 'archive']:
    os.makedirs(os.path.join(settings.STORAGE_ROOT, sub), exist_ok=True)

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
