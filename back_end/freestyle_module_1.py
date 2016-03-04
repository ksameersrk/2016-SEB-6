'''
    API Key: Shiva: AIzaSyB_djwAiUd0Vt3gQgnPxR37gjenE0j3dTU
            Sharon: AIzaSyAZ0yEBve1U580KqocYg-4YwbjoieoriYY
    Part 1
    Retrieve source and destination from front end
    Find places of interest between source and destination and retrieve their location using Client.geocode() - will get lat, long of that place
    
    Part 2
    Compute some logically feasable paths between the source and destination having the places of interest as intermediate points
    
    Part 3
    For each path
    Convert the tuples of lat - long to a road route: use Client.snap_to_road()
    Return this list of paths to the front end
    
    04/03/16
    Module 1
    Get src destination
    Return places
    
    Module 2
    Get places
    Return route
'''

import googlemaps, sys, re
from pprint import pprint

try:
    import urllib2
except:
    print('Run with python2')
    exit()

api_key='AIzaSyCJg4Ezwp-xEMiQlpeuGJxofCL2HOb031s'

url='https://maps.googleapis.com/maps/api/geocode/json?address=__HOLDER__&key=%s' %api_key

gmaps=googlemaps.Client(api_key) # initialize client


def url_translate(address):
   
    return url.replace('__HOLDER__', re.sub(" ", "+", address))


def get_points_of_interest(src, dest):    
   
    src=eval(urllib2.urlopen(url_translate(src)).read())
    src_coord=src['results'][0]['geometry']['location'].values()
    
    dest=eval(urllib2.urlopen(url_translate(dest)).read())
    dest_coord=dest['results'][0]['geometry']['location'].values()
    
    roads=set()
    points_of_interest={}
    
    directions=gmaps.directions(src_coord, dest_coord)
    for s in directions[0]['legs'][0]['steps']:
        roads=roads.union(set(re.findall(r"<b>(.*?)</b>", s['html_instructions'])) - {'north', 'south', 'east', 'west', 'left', 'right'})
    
    for road in roads:
        #print(road)
            
        for result in gmaps.places("tourism near "+road, location=src_coord, radius=directions[0]['legs'][0]['distance']['value'])['results']:
            #print(result['name'])
            try:
                points_of_interest[result['name']]=[result['place_id'], result['geometry']['location'].values(), result['rating']]
            except: 
                continue 	# don't bother with seedy places
           
    sum = 0
    for waypoint, waypoint_details in points_of_interest.items():
        sum = sum + waypoint_details[-1]
    
    avg = sum // len(points_of_interest)
    
    final_result_dict = {}
    
    for waypoint, waypoint_details in points_of_interest.items():
        if waypoint_details[-1] >= avg:
            final_result_dict[waypoint]=waypoint_details
    
    return final_result_dict

if __name__=="__main__":
    #input - source, destination
    #find average rating
    #pull out places with rating greater than the average
    #output - list of places

    user_source = 'Bangalore'
    user_dest = 'Mysore'
    
    pprint(get_points_of_interest(user_source, user_dest))

'''
{u'Bekal Fort': [u'ChIJW4IkcJmApDsRcbLXdzA6qd8',
                 [12.3926108, 75.0327804],
                 4.4],
 u'Brindavan Gardens': [u'ChIJXcr-CeF4rzsRsrbm4H66X5E',
                        [12.4241482, 76.573025],
                        4],
 u'Chimmini Wildlife Sanctuary': [u'ChIJwe-3xrYGqDsRpsZsc7NBRyo',
                                  [10.4310428, 76.4910093],
                                  4.2],
 u'Daria Daulat Bagh': [u'ChIJ1exC-Pp2rzsRV2rHduDbtSQ',
                        [12.4197985, 76.6964914],
                        4.2],
 u'Eco Tourism Park': [u'ChIJb1sq4kR1AjoRZefrzpDLKvI',
                       [22.6021462, 88.4658215],
                       4.5],
 u'GRS Fantasy Park': [u'ChIJiTwfvwhwrzsRnV6SxpQ_T8k',
                       [12.353071, 76.634477],
                       4],
 u'Golden Temple': [u'ChIJUZkS2GCnpTsRSFcZxQwKGNs',
                    [12.4305089, 75.96688240000002],
                    4.5],
 u'India Tourism': [u'ChIJ-Z06a5MVrjsRtwuBKBb7JC0',
                    [12.975417, 77.603083],
                    4.2],
 u'Indian Railway Catering & Tourism Corporation': [u'ChIJbaSfMPU9rjsRn8j7ADxPpck',
                                                    [12.9874449,
                                                     77.56011509999999],
                                                    4.2],
 u'Jungle Lodges Bandipur': [u'ChIJx6tZWYetqDsR3mKc85LA2_Q',
                             [11.7033963, 76.64109069999999],
                             4.6],
 u'Karnataka Tourism': [u'ChIJwXbS4U4VrjsR1fHF9KMZOak',
                        [12.884478, 77.57740199999999],
                        4.4],
 u'Maidan': [u'ChIJT_2mDg53AjoRfo0zRpjT2Kk', [22.5544689, 88.340896], 4.3],
 u'Mangala Devi Temple': [u'ChIJi0C12LtbozsR7PQ8oqAfxYo',
                          [12.8492443, 74.84545849999999],
                          4.6],
 u'Mangalore Port': [u'ChIJqYD9TG9QozsRcxZOAFNJ7SE',
                     [12.9294246, 74.8132315],
                     4.1],
 u'Mysore Palace': [u'ChIJ-aH5AxFwrzsRDdokoeK6f8M',
                    [12.3051351, 76.6551483],
                    4.5],
 u'Mysore Zoo': [u'ChIJlXcOBCNwrzsRy79sy0wzV-o', [12.3024314, 76.663752], 4.3],
 u'Mysore sightseeing': [u'ChIJiTwfvwhwrzsRaQPjQrjlLWM',
                         [12.308724, 76.65307],
                         4.2],
 u'NEW MANGALORE PORT TRUST': [u'ChIJ1SN-R05QozsRynluFK9cBSI',
                               [12.9334069, 74.821225],
                               4.1],
 u'Nagarhole National Park': [u'ChIJU7Z0-K7rpTsRdzegkMNmHz4',
                              [12.0414591, 76.1326491],
                              4.2],
 u'Panambur Beach': [u'ChIJ-SZaaEdQozsR_yP5ureuhUo',
                     [12.937123, 74.80478099999999],
                     4.3],
 u'Pilikula Bioogical Park': [u'ChIJY7LZIGlXozsRahok5OvKCuo',
                              [12.927138, 74.8994089],
                              4],
 u'Rail Museum': [u'ChIJ0zzdpXVwrzsRSsTggeRbyzE',
                  [12.3161707, 76.64345949999999],
                  4.1],
 u'Ranganthittu Bird Sanctuary': [u'ChIJCy4D3Xd3rzsRQ7zik6160t8',
                                  [12.4250211, 76.6535444],
                                  4.3],
 u'Shree Tours and Travels': [u'ChIJKYzmNXcTrjsRjTYDSbJ8Tg0',
                              [12.919045, 77.67088],
                              4.2],
 u'Spice Trip': [u'ChIJUwIzgK96rzsRQKD7RSkhDM8', [12.301093, 76.632556], 4.1],
 u'Sri Kateel Tours & Travels - Tours and Travels in Mangalore': [u'ChIJbfcqdLxQozsRClZbMT8-8X4',
                                                                  [12.925684,
                                                                   74.856403],
                                                                  4.9],
 u'St. Aloysius College': [u'ChIJDW3lKk9aozsRILODU1iHj7g',
                           [12.8730556, 74.8458333],
                           4.2],
 u'Travel Tours': [u'ChIJQREqrUMWrjsR82JbtRQljfE',
                   [12.992661, 77.59483600000002],
                   4.3]}
                   '''
