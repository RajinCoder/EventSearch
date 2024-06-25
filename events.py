import requests

# First get Postal Code from user to display a list of events in the area

API_KEY =  'zcOH2dg6AXZoijhU5NUD4ZlvGdA6cMtG'
base_radius = '1'

url = 'https://app.ticketmaster.com/discovery/v2/events.json'
params = {
    'apikey': API_KEY,
    'radius': base_radius,
    'postalCode': '02115',
    'size': '1'
}

# User Inputs: Postal Code, Radius, City


# Make the request
response = requests.get(url, params=params)
search_results = response.json()

list_events = search_results['_embedded']['events']
list_keys = list_events[0].keys()
print(list_keys)

