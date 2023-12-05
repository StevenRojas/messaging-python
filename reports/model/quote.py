import schema.entities_pb2 as pb
from google.protobuf.wrappers_pb2 import DoubleValue
from google.protobuf.timestamp_pb2 import Timestamp

class Quote:
    def __init__(self, id: str, vin: str, year: int, price: float) -> None:
        self.id = id
        self.vin = vin
        self.year = year
        self.price = price

    @classmethod
    def from_document(instance, doc: dict):
        return instance(
            id=doc['_id'],
            vin=doc['vin'],
            year=doc['year'],
            price=doc['price']['value']
        )
    
class Loader:
    @classmethod
    def vehicle_from_dict(instance, doc: dict) -> pb.Vehicle:
        vehicle = pb.Vehicle()
        vehicle.id = doc['_id']
        vehicle.policy_id = doc['policy_id']
        vehicle.vin = doc['vin']
        vehicle.model = doc['model']
        vehicle.make = doc['make']
        vehicle.year = doc['year']
        vehicle.price.CopyFrom(DoubleValue(value=doc['price']['value']))
        vehicle.last_sold.CopyFrom(Timestamp(seconds=doc['last_sold']['seconds'], nanos=doc['last_sold']['nanos']))
        return vehicle