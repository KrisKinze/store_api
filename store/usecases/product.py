from typing import List, Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from datetime import datetime, timezone
from store.core.exceptions import NotFoundException, InsertException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        try:
            await self.collection.insert_one(product_model.model_dump())
        except Exception as exc:  # noqa: BLE001
            raise InsertException(
                message=f"Error inserting product: {exc}"
            ) from exc

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(
        self, price_min: Optional[float] = None, price_max: Optional[float] = None
    ) -> List[ProductOut]:
        """Query products optionally filtering by price range.

        External API receives price_min/price_max in full value (e.g. 5000 means 5.000 stored).
        We convert by dividing by 1000 to match stored decimal representation.
        Validation: if both provided and price_min >= price_max -> empty result (business rule simplification).
        """
        filters: dict = {}
        if price_min is not None or price_max is not None:
            if price_min is not None and price_max is not None and price_min >= price_max:
                return []
            price_filter = {}
            if price_min is not None:
                price_filter["$gt"] = price_min / 1000
            if price_max is not None:
                price_filter["$lt"] = price_max / 1000
            filters["price"] = price_filter

        return [ProductOut(**item) async for item in self.collection.find(filters)]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        product = await self.collection.find_one({"id": id})

        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        update_data = body.model_dump(exclude_none=True)
        if "updated_at" not in update_data:
            update_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
