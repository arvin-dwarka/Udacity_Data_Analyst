import xml.etree.ElementTree as ET
from pprint import pprint


OSMFILE = 'data/vancouver_canada.osm'

def count_tags(filename):
    '''
    Parse through the OSM file and count the number of tags
    '''
    # initialize dict objects for counter
    tag_count = {}
    
    # iterate through elements
    for _, element in ET.iterparse(filename):
        
        # initiate a count or add a tag to tag_count 
        if element.tag in tag_count:
            tag_count[element.tag] += 1
        else:
            tag_count[element.tag] = 1

        # clear out memory of element for faster processing
        element.clear()             
    return tag_count

if __name__ == "__main__":
    tags = count_tags(OSMFILE)
    pprint(tags)
