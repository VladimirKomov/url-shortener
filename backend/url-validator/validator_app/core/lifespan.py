from validator_app.databases.kafka_consumer import kafka_consumer_client
from validator_app.databases.mongo_db import mongodb_client


async def lifespan_start():
    await mongodb_client.connect()
    await kafka_consumer_client.start_listening()


async def lifespan_shutdown():
    await mongodb_client.close()
    await kafka_consumer_client.shutdown()
