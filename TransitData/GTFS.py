from google.transit import gtfs_realtime_pb2
import time
import requests
import json
import os
from pathlib import Path

class GTFS:
    
    CurrentDirectory = Path(__file__).parent.resolve()
    dataDirectory = os.path.join(CurrentDirectory, "data\\stations.json")
    stationDict = json.load(open(dataDirectory))
    statusDict = {0: 'INCOMING_AT', 1: 'STOPPED_AT', 2: 'IN_TRANSIT_TO'}
    directionDict = {'Glenmont': 0, 'Shady Grove': 1, 'Downtown Largo': 0, 
                     'Franconia-Springfield': 1, 'Vienna': 1, 'New Carrollton': 0, 
                     'Ashburn': 1, 'Huntington': 1, 'Greenbelt': 0, 'Branch Ave': 1}
    
    def cleanStopID(id):
        cleanString = id[3:-2]
        return cleanString

    def getGTFSData(id=None, stationID=None, line=None):
        headers = {'api_key': '1b32768b1e994630bcffe0177cbe4350'}
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get('https://api.wmata.com/gtfs/rail-gtfsrt-vehiclepositions.pb', headers=headers)
        feed.ParseFromString(response.content)
        
        if(id != None):
            trainData = None
            for entity in feed.entity:
                if(entity.vehicle.vehicle.id == id):
                    trainData = entity
            return trainData
        elif(line != None):
            filteredFeed = filter(lambda train: train.vehicle.trip.route_id == line.upper(),feed.entity)
            return list(filteredFeed)
        elif(stationID != None):
            filteredFeed = filter(lambda train: GTFS.cleanStopID(train.vehicle.stop_id) == stationID.upper(),feed.entity)
            return list(filteredFeed)
        else:
            return feed

    def nextStation(trainID, interval):
        train = GTFS.getGTFSData(id=trainID)
        if(train.vehicle.current_status == 1):
            return 'Error'
        while(train.vehicle.current_status != 1):
            time.sleep(interval)
            train = GTFS.getGTFSData(id=trainID)
        return train.vehicle.stop_id
    
    def getDirectionNumber(endpoint):
        return GTFS.directionDict[endpoint]
    

    def getUserTrain(currentStationID,endpoint):
        platformTrains = GTFS.getGTFSData(stationID=currentStationID)
        trainID = 'Error: Train not Found'
        stationDirection = GTFS.getDirectionNumber(endpoint)
        for train in platformTrains:
            if(GTFS.statusDict[train.vehicle.current_status] == 'STOPPED_AT' and train.vehicle.trip.direction_id == stationDirection):
                trainID = train.vehicle.vehicle.id
        return trainID


