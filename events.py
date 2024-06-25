import requests
from format import format_link
from format import format_date
from format import format_time
from format import format_price_range
from format import get

def parse_events(results):
    try:
        events = results['_embedded']['events']
    except:
        return -1
    else:
        for index in range(len(events)):
            EVENT_NAME = get(events, [index, "name"], "TBA")
            EVENT_URL = get(events, [index, "url"], "TBA")
            EVENT_DATE = get(events, [index, "dates", "start", "localDate"], "TBA")
            EVENT_TIME = get(events, [index, "dates", "start", "localTime"], "TBA")
            EVENT_MIN_PRICE = get(events, [index ,"priceRanges", 0, 'min'])
            EVENT_MAX_PRICE = get(events, [index, "priceRanges", 0, 'max'])
            EVENT_CURRENCY = str(get(events, [index, "priceRanges", 0, 'currency']))
            EVENT_PRICE_RANGE = format_price_range(EVENT_MIN_PRICE, EVENT_MAX_PRICE, EVENT_CURRENCY)
            EVENT_VENUE = get(events, [index, "_embedded", "venues", 0, "name"], "TBA")
            EVENT_VENUE_LINK = get(events, [index, "_embedded", "venues", 0, "url"], "TBA")
            print(f"{format_link(EVENT_URL, EVENT_NAME)} | {format_date(EVENT_DATE)} | {format_time(EVENT_TIME)} | {EVENT_PRICE_RANGE} | {format_link(EVENT_VENUE_LINK, EVENT_VENUE)}\n\n")
        
# First get Postal Code from user to display a list of events in the area

API_KEY =  'zcOH2dg6AXZoijhU5NUD4ZlvGdA6cMtG'
url = 'https://app.ticketmaster.com/discovery/v2/events.json'


# User Inputs: Postal Code, Radius, City
#postal_code = input("Enter your Postal Code: ")

search_query = input("Enter preferred choice of search and the corresponding text following: E for event name, P for postal code, and C for city: ")
if search_query[0] == "C" or search_query[0] == "P":
    radius = input("Enter the furthest you're willing to travel: ")

#API Parameters
match search_query[0]:
    case "E":
        params = {'apikey': API_KEY, 'keyword': search_query[1:].strip()}
    case "P":
        params = {'apikey': API_KEY, 'radius': radius, 'postalCode': search_query[1:].strip()}
    case "C":
        params = {'apikey': API_KEY, 'radius': radius, 'city': search_query[1:].strip()}
    case _:
        print("Incorrect format. Try Again")


# Make the request
response = requests.get(url, params=params)


search_results = response.json()
# print(search_results['_embedded']['events'][0])
parse_events(search_results)



# dict_keys(['name', 'type', 'id', 'test', 'url', 'locale', 'images', 'sales', 'dates',
# 'classifications', 'promoter', 'promoters', 'priceRanges', 'seatmap', 'accessibility', 'ticketLimit',
# 'ageRestrictions', 'ticketing', '_links', '_embedded'])


