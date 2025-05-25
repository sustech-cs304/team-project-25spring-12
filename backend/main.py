from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from mjc.utils.database import create_db_and_tables
from mjc.utils.keybuilder import request_key_builder
from mjc.router import user, course, page, widget, common, assignment, folder, argue


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache", key_builder=request_key_builder)
    create_db_and_tables()
    yield


app = FastAPI(root_path='/api/v1', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(course.router)
app.include_router(page.router)
app.include_router(widget.router)
app.include_router(common.router)
app.include_router(assignment.router)
app.include_router(folder.router)
app.include_router(argue.router)

