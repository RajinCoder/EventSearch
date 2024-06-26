import requests
from format import format_link
from format import format_date
from format import format_time
from format import format_price_range
from format import get
import sqlite3

conn = sqlite3.connect('events.db')
cursor = conn.cursor()

def print_events(events):
    for i in range(len(events)):
        event = events[i]
        print(f'{str(i + 1)} | {format_link(event["url"], event["name"])} | {format_date(event["date"])} | {format_time(event["time"])} | {event["price_range"]} | {format_link(event["venue_link"], event["venue"])}\n')

def parse_events(results):
    try:
        events = results['_embedded']['events']
    except:
        return -1
    else:
        for index in range(len(events)):
            EVENT_ID = get(events, [index, "id"])
            EVENT_NAME = get(events, [index, "name"], "TBA")
            EVENT_URL = get(events, [index, "url"], "TBA")
            EVENT_DATE = get(events, [index, "dates", "start", "localDate"], "TBA")
            EVENT_TIME = get(events, [index, "dates", "start", "localTime"], "TBA")
            EVENT_MIN_PRICE = get(events, [index ,"priceRanges", 0, 'min'])
            EVENT_MAX_PRICE = get(events, [index, "priceRanges", 0, 'max'])
            EVENT_CURRENCY = str(get(events, [index, "priceRanges", 0, 'currency']))
            EVENT_PRICE_RANGE = format_price_range(EVENT_MIN_PRICE, EVENT_MAX_PRICE, EVENT_CURRENCY)
            EVENT_VENUE = get(events, [index, "_embedded", "venues", 0, "name"], "TBA")
            EVENT_VENUE_LINK = get(events, [index, "_embedded", "venues", 0, "url"])
            events[index] = {
                "event_id": EVENT_ID,
                "name": EVENT_NAME,
                "url": EVENT_URL,
                "date": EVENT_DATE,
                "time": EVENT_TIME,
                "price_range": EVENT_PRICE_RANGE,
                "venue": EVENT_VENUE,
                "venue_link": EVENT_VENUE_LINK
            }
        return events
# dict_keys(['name', 'type', 'id', 'test', 'url', 'locale', 'images', 'sales', 'dates',
# 'classifications', 'promoter', 'promoters', 'priceRanges', 'seatmap', 'accessibility', 'ticketLimit',
# 'ageRestrictions', 'ticketing', '_links', '_embedded'])

API_KEY =  'zcOH2dg6AXZoijhU5NUD4ZlvGdA6cMtG'
url = 'https://app.ticketmaster.com/discovery/v2/events.json'

def perform_search(username, user_id):
    # Loop till ended by User
    programOver = False

    while not programOver:
        print(f"@{username}/search >")
        # User Inputs: Postal Code, Radius, City
        search_query = input(" \t E - by event name \n \t P - by postal code \n \t C - by city \n \t B - go back \n \t Q - quit program \n \t Enter preferred search filter and the corresponding text following: ")
        if search_query[0] == "C" or search_query[0] == "P":
            radius = input("\t Enter the furthest you're willing to travel: ")

        #API Parameters
        match search_query[0]:
            case "E":
                params = {'apikey': API_KEY, 'keyword': search_query[1:].strip()}
                
            case "P":
                params = {'apikey': API_KEY, 'radius': radius, 'postalCode': search_query[1:].strip()}
                
            case "C":
                params = {'apikey': API_KEY, 'radius': radius, 'city': search_query[1:].strip()}
            case "B":
                return
            case "Q":
                programOver = True
                break
            case _:
                print("Incorrect format. Try Again")
                continue

        # Make the request
        response = requests.get(url, params=params)
        search_results = response.json()
        events = parse_events(search_results)
        print_events(events)

        print(f"@{username}/search >")
        option = input(" \t F - add to favorites (followed by which option to favorite) \n \t S - perform a new search \n \t B - go back \n \t Q - quit program \n \t Please pick an option: ")
        match option[0]:
            case "F":
                favorite_option = int(option[1:].strip())
                add_favorite(user_id, events[favorite_option - 1])
            case "S":
                continue
            case "B":
                return
            case "Q":
                programOver = True
                break
            case _:
                print("Incorrect format. Try Again")
                continue 

def add_favorite(user_id, event):
    # cursor.execute(f'SELECT * FROM event_favorites WHERE user_id = ${user_id} AND event_id = \'{event["event_id"]}\'')
    # if len(cursor.fetchall()) > 0:
    #     print("Already added to favorites")
    #     return
    cursor.execute(f'INSERT INTO event_favorites (user_id, event_id) VALUES ({user_id}, \'{event["event_id"]}\')')
    conn.commit()
    cursor.execute(f'SELECT * FROM event WHERE event_id = \'{event["event_id"]}\'')
    if len(cursor.fetchall()) == 0:
        cursor.execute(f'INSERT INTO event (event_id, date, name, url, price_range, time, venue, venue_link) VALUES (\'{event["event_id"]}\', \'{event["date"]}\', \'{event["name"]}\', \'{event["url"]}\', \'{event["price_range"]}\', \'{event["time"]}\', \'{event["venue"]}\', \'{event["venue_link"]}\')')   
        conn.commit()
    print("Added to favorites")

def remove_favorite(user_id, event):
    cursor.execute(f'DELETE FROM event_favorites WHERE user_id = {user_id} and event_id = \'{event["event_id"]}\'')
    conn.commit()
    print("Removed favorites")


def display_favorites(username, user_id):
    cursor.execute(f'SELECT event.event_id, event.name, event.url, event.date, event.time, event.price_range, event.venue, event.venue_link FROM event INNER JOIN event_favorites ON event.event_id=event_favorites.event_id WHERE event_favorites.user_id = {user_id}')
    events = cursor.fetchall()
    if not events:
        print("You currently don't have any favorites")
        return;
    for i in range(len(events)):
        events[i] = {
            "event_id": events[i][0],
            "name": events[i][1],
            "url": events[i][2],
            "date": events[i][3],
            "time": events[i][4],
            "price_range": events[i][5],
            "venue": events[i][6],
            "venue_link": events[i][7]
        }
    print("Favorites: ")
    print_events(events)
    print(f"@{username}/favorites >")
    option = input(" \t R - remove from favorites (followed by which option to remove) \n \t B - go back \n \t Q - quit program \n \t Please pick an option: ")
    match option[0]:
        case "R":
            favorite_option = int(option[1:].strip())
            remove_favorite(user_id, events[favorite_option - 1])
        case "B":
            return
        case _:
            return

def display_user_options(username, user_id):
    programOver = False
    while not programOver:
        print(f"@{username} >")
        option = input(" \t S - open up search menu \n \t F - display favorites \n \t Q - quit program \n \t Please pick an option: ")

        match option:
            case "S":
                perform_search(username, user_id)
            case "F":
                display_favorites(username, user_id)
            case "Q":
                programOver = True
                break
            case _:
                print("Incorrect format. Try Again")
                continue