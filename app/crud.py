from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from app.database import Advertisement
from app.schemas import AdCreate, AdResponse, AdUpdate
from sqlalchemy import select, update, delete

async def create_ad(session: AsyncSession, ad: AdCreate) -> AdResponse:
    ad = Advertisement(
        title=ad.title,
        description=ad.description,
        price=ad.price,
        author=ad.author,
    )
    session.add(ad)
    
    try:
        await session.commit()
    except IntegrityError as err:
        raise HTTPException(409, "Item already exists")
    await session.refresh(ad)
    return AdResponse.model_validate(ad)

async def get_ad(session: AsyncSession, ad_id: int) -> AdResponse:
    ad = await session.get(Advertisement, ad_id)
    if ad is None:
        raise HTTPException(404, f"Ad not found")
    return AdResponse.model_validate(ad)

async def update_ad(session: AsyncSession, ad_id: int, ad: AdUpdate) -> AdResponse:
    adwert = await session.get(Advertisement, ad_id)
    if adwert is None:
        raise HTTPException(404, f"Ad not found")
    if ad.title is not None:
        adwert.title = ad.title
    if ad.description is not None:
        adwert.description = ad.description
    if ad.price is not None:
        adwert.price = ad.price
    if ad.author is not None:
        adwert.author = ad.author
    await session.commit()
    await session.refresh(adwert)
    return AdResponse.model_validate(adwert)

async def delete_ad(session: AsyncSession, ad_id: int):
    ad = await session.get(Advertisement, ad_id)
    if ad is None:
        raise HTTPException(404, f"Ad not found")
    await session.delete(ad)
    await session.commit()
    return status.HTTP_204_NO_CONTENT

async def search_ad(
    session: AsyncSession,
    title: str | None = None,
    description: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    author: str | None = None) -> list[AdResponse]:
    statement = select(Advertisement)
    if title is not None:
        statement = statement.where(Advertisement.title.ilike(f"%{title}%"))
    if description is not None:
        statement = statement.where(Advertisement.description.ilike(f"%{description}%"))
    if price_min is not None:
        statement = statement.where(Advertisement.price >= price_min)
    if price_max is not None:
        statement = statement.where(Advertisement.price <= price_max)
    if author is not None:
        statement = statement.where(Advertisement.author.ilike(f"%{author}%"))
    result = await session.execute(statement)
    ads = result.scalars().all()
    return [AdResponse.model_validate(ad) for ad in ads]