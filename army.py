import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv

import chime
import aiohttp

chime.theme("zelda")

maxDateRemoteFormat = "2026-07-15T00:00:00.000Z"
load_dotenv()
TOKEN = os.getenv('access_token')

url = "https://as-portal-a-prod884f86a.azurewebsites.net/graphql"

data = {
    "operationName": "startHousingReservation",
    "variables": {
        "input": {
            "houseId": "HK32-52",
            "collectiveHouseIds": [],
            "language": "en"
        }
    },
    "query": """
    mutation startHousingReservation($input: StartHousingReservationInput!) {
      startHousingReservation(input: $input) {
        ... on StartHousingReservationSuccessPayload {
          reservationIds
          __typename
        }
        ... on StartHousingReservationErrorPayload {
          errorMessage {
            errorCode
            parameters {
              parameter
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
    }
    """
}

headers = {
    "Authorization": "Bearer {}".format(TOKEN)}


async def send_request(session):
    try:
        async with session.post(url, json=data, headers=headers) as response:
            result = await response.json()
            payload = result["data"]["startHousingReservation"]

            
            if "reservationIds" in payload:
                print("SUCCESS!", payload)

                # Play success sound
                chime.success()

                return True
            else: 
                print(payload)
    except Exception as e:
        print("Error:", e)


async def main():
    target_time = datetime(2026, 5, 12, 23, 59, 59)

    # Wait until target time
    while datetime.now() < target_time:
        await asyncio.sleep(0.01)

    async with aiohttp.ClientSession() as session:
        while True:
            asyncio.create_task(send_request(session))
            await asyncio.sleep(0.1)


asyncio.run(main())
