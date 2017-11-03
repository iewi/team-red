'''

This module defines classes for geographic areas. The classes defined are: tract and district.

A tract object represents a census tract. Specifically, it stores its
* population (int)
* ID (str)
* adjacent tracts (list of tracts)

A district object represents a congressional district. It stores
* population (int)
* component tracts (list of tracts)

This module also includes a sample method to retrieve data to set up a tract object

CHANGE LOG
Dorothy Carter - 20171028 - initial creation of classes & script

'''


class tract:
    def __init__(self, pop=0, tract_id=""):
        '''
        this initializes a tract object.
        arguments: pop (=population of tract). Int. Default 0
                   tract_id. Str. Default 0
        sets the adjacent_to attribute to an empty list
        '''
        self.population = pop
        self.id = tract_id
        self.adjacent_to = []
    
    def add_adjacency(self, tract):
        '''
        this appends a tract to the list of adjacent tracts
        
        arguments: tract. A str (the tract id). No default
        '''
        
        self.adjacent_to.append(tract)
    
    def set_adjacencies_to(self, areas):
        '''
        this is a convenience to set the adjacent_to attribute to a new list
        provided in case extra processing has to go here
        
        arguments: areas. A list of tract ids (strs) it is adjacent to. No default
        '''
        
        self.adjacent_to = areas
        
    def bulk_add_adjacencies(self, tracts):
        '''
        this appends a list of tracts to the list of adjacent tracts
        
        arguments: tracts. A list of tract ids (strs) it is adjacent to. No default
        '''
        
        self.adjacent_to.extend(tracts)
   
    def get_adjacencies(self):
        '''
        this returns the adjacent_to list. not strictly necessary (could use self.adjacent_to),
        but provided as a convenience
        
        can use as:
        for tract in this_tract.get_adjacencies():
            pass
        '''
        return self.adjacent_to
   
    def __str__(self):
        '''
        this prints the tract object nicely.
        '''
        return "Census tract " + self.id + ". Population: " + str(self.population)

class district:
    def __init__(self, pop=0):
        '''
        this initializes a tract object.
        arguments: pop (=population of tract). Int. Default 0
        sets the tracts attribute to an empty list
        '''
        self.population = pop
        self.tracts = []
    
    def add_tract(self, tract_id, tract_pop):
        '''
        this initializes a new tract object and adds it to the tracts list
        arguments: tract_id. Str. No default
                   tract_pop (=population of tract). Int. No default
        '''
        self.tracts.append( tract(tract_pop, tract_id) )
    
    def add_tract(self, tract):
        '''
        this adds a previously created tract object to the tracts list
        arguments: tract. A tract object. No default
        '''
        self.tracts.append(tract)
   
    def bulk_add_tract(self, many_tracts):
        '''
        this adds a list of tracts to the component tracts
        arguments: many_tracts. A list of tracts. No default
        '''
        self.tracts.extend(many_tracts)
        
    def set_tracts_to(self, new_tracts):
        '''
        this sets the list of component tracts to the list passed in
        arguments: new_tracts. A list of tracts. No default
        '''
        self.tracts = new_tracts
   
    def get_tracts(self):
        '''
        this returns the list of component tracts. not strictly necessary (use self.tracts),
        but provided as a convenience
        '''
        return self.tracts
        
    def __str__(self):
        '''
        this prints the district object nicely
        '''
        return "District population: " + str(self.population) + ". " + str(len(self.tracts)) + " included"


# here begins a sample of how to set up a tract object
import json
import csv # ...
import re

from urllib import urlopen
from constants import api_key

def get_adjacent_tracts(tract):
    # this gets just the tract ids, not county ids or state codes
    # first two chars are 24, then 3 chars for county code. then tract id
    tract_regex = re.compile("^24\d{3}(\d{6})$")
    
    with open("./tracts/md_adj_tracts.csv", "r") as tracts_csv:
        reader = csv.DictReader(tracts_csv)
        ids = []
        for row in reader:
            row_match = tract_regex.match(row['SOURCE_TRACTID'])
            if row_match.group(1) == tract.id:
                adj_match = tract_regex.match(row['NEIGHBOR_TRACTID'])
                ids.append(adj_match.group(1))
        
        tract.bulk_add_adjacencies(ids)
        
    return tract

def set_up_tract():
    # this url gets population 18 years & older for one tract in MD
    url = "https://api.census.gov/data/2010/sf1?get=P0100001&for=tract:000100&in=state:24&in=county:001&key=" + api_key
    
    response = urlopen(url)
    if response.getcode() != 200:
        print "URL opening did not go too well. HTTP status code: " + str(response.getcode())
    else:
        data = json.load(response)
        # sorry. the census api hands back deficient json
        my_tract = tract( int(data[1][0]), data[1][3] )
        my_tract = get_adjacent_tracts(my_tract)
        print "Here is our tract: " + str(my_tract)
        print "Here is the first adjacent tract: " + str(my_tract.adjacent_to[0])
        print "Here is the length of adjacent tracts: " + str(len(my_tract.adjacent_to))

