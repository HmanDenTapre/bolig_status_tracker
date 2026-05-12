import requests
import time
import chime
from datetime import datetime
chime.theme('zelda') # Options: 'chime', 'mario', 'zelda'

mode = 0 # Options: 0=simple, 1=desperate
debug = False
delay = 60 # Time between requests in seconds

#[{"parent":"Trondheim","children":["Moholt"]}]
location = [{"parent":"Trondheim", "children":[]}]
maxDateRemoteFormat = "2026-07-15T00:00:00.000Z"
maxDate = datetime.fromisoformat(maxDateRemoteFormat.replace("Z", "+00:00"))

url = "https://as-portal-a-prod884f86a.azurewebsites.net/graphql"
data = {
    "operationName": "GetHousingIds",
    "variables": {
        "input": {
            "location": location,
            "availableMaxDate": maxDateRemoteFormat,
            "showUnavailable": False if mode == 0 else True,
            "residenceCategories": ["3-roms"],
            "offset": 0,
            "pageSize": 10,
            "includeFilterCounts": True,
            "shuffleSeed": 20084
        }
    },
    "query": """query GetHousingIds($input: GetHousingsInput!) {
        housings(filter: $input) {
            housingRentalObjects {
                rentalObjectId
                isAvailable
                availableFrom
                availableTo
                hasActiveReservation
            }
            filterCounts {
                locations { key value }
                residenceCategories { key value }
                categories { key value }
                notAvailableCount
            }
            totalCount
        }
    }"""
}

prospectDict = {} # Might be available before semester start
availableDict = {}

cycles = 0
chime.success(True) # Test audio
while True:
    rtnObj = requests.post(url, json=data)
    if debug:
        print(rtnObj.status_code)
        print(rtnObj.text)
    elif rtnObj.status_code != 200:
        print(f"Error code: {rtnObj.status_code}")
    objJson = rtnObj.json()
    housingObjs = objJson["data"]["housings"]["housingRentalObjects"]
    if mode==0:
        if len(housingObjs) > 0:
            print(f"\n({datetime.now()}) -------")
            chime.success(True)
            for obj in housingObjs:
                print(f"Housing {obj["rentalObjectId"]} is now available")
    elif mode==1:
        print("")
    if cycles % 10 == 0:
        print(f"Logging ---------- {datetime.now()}")
    cycles += 1
    time.sleep(delay)
