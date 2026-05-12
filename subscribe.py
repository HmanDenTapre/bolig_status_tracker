import requests
import json
import time
import chime
from datetime import datetime

import asyncio
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

chime.theme('zelda') # Options: 'chime', 'mario', 'zelda'

# IDs to monitor
reservation_ids = [
    "HK46-32"
]

# Websocket endpoint
transport = WebsocketsTransport(
    url="wss://as-portal-a-prod884f86a.azurewebsites.net/graphql"
)

# GraphQL subscription
data = gql("""
subscription($id: String!) {
  housingReservationUpdated(id: $id) {
    id
    state
    lastModifiedDate
    reservationExists
  }
}
""")

async def subscribe_to_reservation(session, reservation_id):

    print(f"Starting subscription for {reservation_id}")

    async for result in session.subscribe(
        data,
        variable_values={"id": reservation_id}
    ):
        chime.success(True)
        print(f"\nUpdate for {reservation_id}")
        print(result)

async def main():

    chime.success(True) # Test audio

    async with Client(
        transport=transport,
        fetch_schema_from_transport=False,
    ) as session:

        tasks = []

        for reservation_id in reservation_ids:
            task = asyncio.create_task(
                subscribe_to_reservation(session, reservation_id)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)

asyncio.run(main())