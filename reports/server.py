import sys
from dotenv import load_dotenv
import pymongo
import os
import signal
import asyncio
from repository.repository import Repository
import datetime

async def serve():
    load_dotenv()
    print("Starting server...")
    client = await connect_mongodb()
    print("Connected to MongoDB")
    repo = Repository(client, "policies")
    quotations = await repo.get_quotation_list("7d9c9dd9-5052-4865-a077-f0fa1463d45a")
    for quotation in quotations:
        quote = await repo.get_quotation(quotation.id)
        quote.last_sold.FromDatetime(datetime.datetime.now())
        quote.year = 2021
        print(quote)
        await repo.update_quotation(quote)

async def stop():
    print("Stopping server...")

async def connect_mongodb():
    host = os.getenv("MONGO_HOST")
    if not host:
        print("MONGO_HOST environment variable not set")
        sys.exit(1)
    print("Connecting to MongoDB...", host)
    try:
        client = pymongo.MongoClient(host, serverSelectionTimeoutMS=1)
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Could not connect to MongoDB", err)
        sys.exit(1)
    except Exception as err:
        print("Something went wrong", err)
        sys.exit(1)
    return client

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(serve())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(stop())
        loop.close()
        sys.exit(0)