import xml.etree.cElementTree as ET
from collections import defaultdict
import re
from pprint import pprint

OSMFILE = 'data/vancouver_canada.osm'
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Hwy": "Highway",
            "Hwy.": "Highway",
            "Moncton": "Moncton Street",
            "Pender": "Pender Street",
            "Tsawwassen": "North Tsawwassen",
            "av": "Avenue",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Edmonds": "Edmonds Street",
            "Hastings": "Hastings Street",
            "Blvd": "Boulevard",
            "Jervis": "Jarvis"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    elem.clear()
    return street_types

def update_name(name, mapping):
    try:
        street_name = name.split(' ')
        street_name[-1] = mapping[street_name[-1]]
        return ' '.join(street_name)

    except KeyError:
        mapping['name'] = 'name'
        return name

if __name__ == '__main__':
    st_types = audit(OSMFILE)
    pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
