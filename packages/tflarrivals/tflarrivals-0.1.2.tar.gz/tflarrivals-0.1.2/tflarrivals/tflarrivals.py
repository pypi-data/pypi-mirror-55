import requests
import json
import bisect

def search_stations_by_common_name(name) -> list:
    '''
    Search TfL API for stations matching name
    Args:
        name (str): The common name to search for,
    
    Returns:
        stations (list): A list of stations matching name,
    '''
    resp = requests.get(f"https://api.tfl.gov.uk/StopPoint/Search?query={name}")
    matches_full = json.loads(resp.text)
    matches = []
    for match in matches_full["matches"]:
        matches.append({
            "name": match["name"],
            "modes": match["modes"],
            "id": match["id"]
        })
    return matches

class Station:
    '''
    The Station object stores data relating to a station

    Args:
        id (str): The station id, can be found using search_stations_by_common_name

    Attributes:
        id (str): Station id,
        station_dict (dict): Raw dictionary data loaded from TfL API,
        name (str): Station's common name,
        stops (list): List of stops in this station,
    '''
    def __init__(self, id):
        self.id = id
        resp = requests.get(f"https://api.tfl.gov.uk/StopPoint/{id}")
        self.station_dict = json.loads(resp.text)
        self.name = self._get_name()
        self.stops = self._get_stops()
    
    def _get_stops(self):
        '''
        Gets stops in station
        '''
        stops = []
        for child in self.station_dict["children"]:
            stops.append(Stop(child))
        if stops:
            return stops
    
    def _get_name(self):
        '''
        Gets common name of station
        '''
        return self.station_dict["commonName"]

    def __repr__(self):
        return f"{self.name}. ID: {self.id}"
    
    def __str__(self):
        return self.__repr__()
        
class Stop:
    '''
    The Stop object stores data relating to a stop, should only be called by Station.

    Args:
        stop_dict (dict): Raw dictionary of stop info from TfL API,

    Attributes:
        id (str): Stop id,
        stop_dict (dict): Raw dictionary data loaded from TfL API,
        name (str): Stop's common name,
    '''
    def __init__(self, stop_dict):
        self.stop_dict = stop_dict
        self.id = stop_dict["naptanId"]
        self.direction = self._get_direction()
        self.name = stop_dict["commonName"]
    
    def get_arrivals(self):
        '''
        Gets arrivals of services to this stop
        '''
        return Arrivals(self.id)

    def _get_direction(self):
        '''
        Gets direction of this stop
        '''
        additional_props = self.stop_dict["additionalProperties"]
        for prop in additional_props:
            if prop["category"] == "Direction" and prop["key"] == "Towards":
                return prop["value"]
        return None
    
    def __repr__(self):
        if self.direction is not None:
            return f"{type(self)}: {self.name}. Towards: {self.direction}. ID: {self.id}"
        return f"<{type(self)} Object: {self.name}. ID: {self.id}"

class Arrivals(dict):
    '''
    The Arrivals object stores all arrivals at a stop in a dictionary format. Top level
    keys are lines, then platforms, then arrivals including destination name. Arrival
    times are in seconds.

    Args:
        stop_id (str): Stop id fetched from TfL API, can be found with a combination 
                       of search_stations_by_common_name and Station

    Attributes:
        stop_id (str): Stop id,
    '''
    def __init__(self, stop_id):
        dict.__init__(self)
        self.stop_id = stop_id
        self.update()

    def update(self):
        '''
        Updates self with all arrivals at this station.
        '''
        resp = requests.get(f"https://api.tfl.gov.uk/StopPoint/{self.stop_id}/Arrivals")
        arrival_list_full = json.loads(resp.text)
        arrival_dict = self
        for arrival in arrival_list_full:
            line_name = arrival["lineName"]
            if arrival["modeName"] == "tube":
                line_name += " Line"
            if line_name not in arrival_dict.keys():
                arrival_dict[line_name] = {}
            platform_name = arrival["platformName"]
            if platform_name not in arrival_dict[line_name].keys():
                arrival_dict[line_name][platform_name] = {}
            destination_name = arrival["destinationName"]
            eta = arrival["timeToStation"]
            arrival_dict[line_name][platform_name][eta] = destination_name
