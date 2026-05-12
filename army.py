import requests
import time
import chime
from datetime import datetime
chime.theme('zelda') # Options: 'chime', 'mario', 'zelda'

maxDateRemoteFormat = "2026-07-15T00:00:00.000Z"

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
  "query": "mutation startHousingReservation($input: StartHousingReservationInput!) {\n  startHousingReservation(input: $input) {\n    ... on StartHousingReservationSuccessPayload {\n      reservationIds\n      __typename\n    }\n    ... on StartHousingReservationErrorPayload {\n      errorMessage {\n        errorCode\n        parameters {\n          parameter\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"}

# 2026-05-12 23:24:39.737185
while True: 
    if datetime.now() > datetime(2026,5,12,23,59,59): 
        rtnObj = requests.post(url, json=data)
        time.sleep(0.1);


