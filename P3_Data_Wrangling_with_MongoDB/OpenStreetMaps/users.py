import xml.etree.ElementTree as ET
from pprint import pprint


OSMFILE = 'data/vancouver_canada.osm'

def unique_users(filename):
    '''
    Parse through the file and count the number of unique contributors
    '''
    users = set()
    for _, element in ET.iterparse(filename):
        try:
            users.add(element.attrib['uid'])
        except KeyError:
            pass
        element.clear()
    return users

if __name__ == "__main__":
    users = unique_users(OSMFILE)
    pprint(len(users))