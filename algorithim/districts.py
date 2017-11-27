'''

this module creates a district out of tracts. it contains two main methods:
generic_redistrict - re-district Maryland using a default start
specific_redistrict - given a starting tract, re-district Maryland

and two 'helper' methods:
_take_tract - remove a tract from available_tracts, and return false if that fails
_create_district - given a starting tract, create a congressional district

ISSUES
fragments - after creating most districts, only a few remain. they are
            unsuitable for another district, being possibly non-adjacent
            and/or not having enough population to make another one

validity - check the resulting districts for population parity. if not
           within a certain margin of error, discard this districting

infinite loop - if no adjacent tracts are available, create_district
                will loop forever

number of districts - Maryland is only assigned 8 congressional districts,
                      but this (as currently implemented) may create more
                      or fewer. should be easy to fix (maybe)

CHANGE LOG
Dorothy Carter - 20171109 - initial creation  
Dorothy Carter - 20171127 - initial work on expanding method         

'''

import random

import tracts
import geography_objects

# average number of people in an MD congressional district
MAGIC_POPULATION_NUMBER = 723741

# every census tract in md
all_tracts = tracts.get_all_tracts()
available_tracts = [k for k in all_tracts.values()]

def _take_tract(tractid):
    '''
    tries to remove a tract denoted by tractid. returns True
    if success, False if failure
    '''
    try:
        available_tracts.remove(tractid)
        return True
    except ValueError:
        return False


def _create_district(start):
    '''
    this creates one congressional district given a starting tract
    
    it queues all adjacent tracts for the start, then from the first, etc
    and grabs them sequentially until the district is made. It takes the next
    
    
    arguments: start - a tract object from which districting starts
    returns: a district object representing the finished district
    '''
    
    # tries to add the passed-in starting tract to the district
    # will raise an exception if the district is already taken
    created_district = geography_objects.district()
    if _take_tract(start.id):
        created_district.add_tract(start)
    else:
        raise geography_objects.district_error("starting tract is already taken")
    
    # queue up all adjacent tracts to the start
    queue = set()
    for t in start.adjacent_to:
        queue.add(t)
    
    # this loop keeps trying to add tracts until the district hits
    # its population target. see ISSUES above for the potential 
    # infinite loop issue
    while created_district.population <= MAGIC_POPULATION_NUMBER:
        next = all_tracts[queue.pop()] # dequeue the first tract
        if _take_tract(next):
            created_district.add_tract(next)
            # queue all tracts adjacent
            # since queue is a set, no dupes
            for t in next.adjacent_to:
                queue.add(t)  
    
    return created_district
    

def generic_redistrict():
    '''
    this redistricts Maryland using a default start tract
    returns:
    '''
    start = all_tracts["751200"]
    return specific_redistrict(start)

def specific_redistrict(start):
    '''
    this redistricts Maryland using a given start tract
    arguments: start - a tract object that districting will start from
    returns: 
    '''
    return "not implemented"
