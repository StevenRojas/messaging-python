from pymongo import MongoClient
from model.quote import Quote
import schema.entities_pb2 as pb
from model.quote import Loader

quotations_collection_name = "quotes"

class Repository:
    def __init__(self, client: MongoClient, db: str):
        self.client = client
        self.db = self.client[db]
        self.quotations_collection = self.db[quotations_collection_name]

    async def get_quotation_list(self, policy_id: str) -> list[Quote]:
        filter = {'policy_id': policy_id, 'price.value': {'$gte': 15000}}
        projection = {'vin':1, 'year':1, 'price':1}
        cursor = self.quotations_collection.find(filter, projection)
        result = []
        for quotation in cursor:
            result.append(Quote.from_document(quotation))
        return result

    async def get_quotation(self, quotation_id: str) -> pb.Vehicle:
        filter = {'_id': quotation_id}
        projection = {}
        quotation = self.quotations_collection.find_one(filter, projection)
        print(quotation)
        vehicle = Loader.vehicle_from_dict(quotation)

        return vehicle
    
    async def update_quotation(self, quotation: pb.Vehicle) -> None:
        filter = {'_id': quotation.id}
        update = {
            '$set': {
                'year': quotation.year,
                'price.value': quotation.price.value
            }
        }
        self.quotations_collection.update_one(filter, update)