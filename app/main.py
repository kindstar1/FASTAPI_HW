from fastapi import FastAPI

import app.crud as crud
from app.schemas import (AdCreate, AdResponse, AdUpdate)
from app.dependencies import SessionDependency
from app.database import init_orm, close_orm

app = FastAPI(
    title='Advertisement API',
)


@app.post('/advertisement', response_model=AdResponse)
async def create_ad(ad: AdCreate, session: SessionDependency):
    return await crud.create_ad(session, ad)


@app.get('/advertisement/{ad_id}', response_model=AdResponse)
async def get_ad(ad_id: int, session: SessionDependency):
    return await crud.get_ad(session, ad_id)


@app.patch('/advertisement/{ad_id}', response_model=AdResponse)
async def update_ad(ad_id: int, ad_data: AdUpdate, session: SessionDependency):
    return await crud.update_ad(session, ad_id, ad_data)


@app.delete('/advertisement/{ad_id}', status_code=204)
async def delete_ad(ad_id: int, session: SessionDependency):
    return await crud.delete_ad(session, ad_id)

@app.get('/advertisement', response_model=list[AdResponse])
async def search_ad(session: SessionDependency, title: str | None = None, description: str | None = None, price_min: float | None = None, price_max: float | None = None, author: str | None = None):
    return await crud.search_ad(session, title, description, price_min, price_max, author)

@app.on_event("startup")
async def startup():
    await init_orm()

@app.on_event("shutdown")
async def shutdown():
    await close_orm()
