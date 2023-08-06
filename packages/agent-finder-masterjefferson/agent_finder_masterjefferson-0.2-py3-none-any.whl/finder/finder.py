from finder import gmaps
import logging
import subprocess
import time
import csv
import argparse

"""
Logger configuration
"""

logging.basicConfig(format='%(asctime)s | %(message)s', datefmt='%m/%d/%y %H:%M:%S %p')
log = logging.getLogger("agent-finder")
log.setLevel(logging.INFO)

"""
Keys of interest in a place detail dictionary returned from google maps. These are also the keys used 
to write the insurance agent details to the output CSV file.
"""
place_detail_keys = ['name', 'formatted_address', 'formatted_phone_number', 'website', 'rating']


def to_agent(details):
    """
    Convert googlemaps place details dictionary to an 'agent' dictionary.
    :param details: Place details dict retrieved from googlemaps.Client.place()
    :return: An 'agent' dictionary with place_details_keys as key values.
    """
    agent = {place_detail_keys[i]: "N/A" for i in range(0, len(place_detail_keys))}
    for key in place_detail_keys:
        if key in details:
            agent[key] = details[key]
    return agent


def print_agent(agent):
    """
    Debug log an agent dictionary.
    :param agent: A dictionary containing keys from place_details_keys
    """
    agent_string = "FOUND:\n"
    for key in place_detail_keys:
        agent_string += "\t%s: %s\n" % (key, agent[key])
    log.debug(agent_string)


def agent_search(location, radius_km):
    """
    Look up details of all auto insurance agents for the given location.
    :param location: A location dictionary (lat/long).
    :param radius_km: Search radius in kilometers.
    :return: A list of agent dictionaries.
    """
    pg_token = None
    token_key = 'next_page_token'
    agents = []
    while True:
        places_resp = gmaps.places('auto insurance', location=location, radius=1000 * radius_km, type='insurance_agent',
                                   page_token=pg_token)
        results = places_resp['results']
        for res in results:
            details = gmaps.place(res['place_id'])['result']
            agent = to_agent(details)
            agents.append(agent)
            print_agent(agent)
        if token_key in places_resp:
            pg_token = str(places_resp[token_key])
            time.sleep(2)
        else:
            break
    return agents


def geocode_to_point(location):
    """
    Geocode a plain text location query to a physical location.
    :param location: The location query string.
    :return: Location dictionary (lat/long)
    """
    geocoded = gmaps.geocode(location)
    point = geocoded[0]['geometry']['location']
    return point


def write_to_csv(agents, filename):
    """
    Write a list of agent dictionaries to a CSV file.
    :param agents: The list of agents dicts.
    :param filename: The name of the output file
    """
    log.info("Writing CSV file '%s'..." % filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=place_detail_keys)
        writer.writeheader()
        writer.writerows(agents)


def main():
    parser = argparse.ArgumentParser(description="Search for insurance agents by location.")
    parser.add_argument('location', help='search location')
    parser.add_argument('--radius', default=15, type=int, help='search radius in kilometers')
    parser.add_argument('--filename', default='output.csv', help='output filename')
    args = parser.parse_args()
    log.info("Finding auto insurance agents in '%s'... (radius = %d km)" % (args.location, args.radius))
    point = geocode_to_point(args.location)
    agents = agent_search(point, args.radius)
    log.info("Done! Found %d agents." % len(agents))
    write_to_csv(agents, args.filename)
    subprocess.run(["open", args.filename])
