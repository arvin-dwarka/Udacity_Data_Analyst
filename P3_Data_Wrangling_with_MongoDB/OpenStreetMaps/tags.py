import xml.etree.ElementTree as ET
from pprint import pprint
import re


OSMFILE = 'data/vancouver_canada.osm'

# create three regex to check data source
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    '''
    Runs a count of tag types for lower, lower_colon and problemchars
    '''
    if element.tag == "tag":
        key = element.get('k')
        if re.search(lower, key):
            keys['lower'] += 1
        elif re.search(lower_colon, key):
            keys['lower_colon'] += 1
        elif re.search(problemchars, key):
            keys['problemchars'] += 1    
        else:
            keys['other'] += 1
        
    return keys

def process_map(filename):
    '''
    Parse through the file and initialiate key type count
    '''
	# initialize dict
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

        #clear element from memory for faster processing
        element.clear()

    return keys

if __name__ == "__main__":
    tags = process_map(OSMFILE)
    pprint(tags)
