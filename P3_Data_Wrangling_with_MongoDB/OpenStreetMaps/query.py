from pymongo import MongoClient
from pprint import pprint


def get_db():
    client = MongoClient('localhost:27017')
    db = client.van
    return db

def top_user():
    """
    returns user with most contributions
    """
    return [{
        '$group': {
            '_id': '$created.user',
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    }, {
        '$limit': 1
    }]

def single_post_users():
    """
    returns number of users contributing only once
    """
    return [{
        '$group': {
            '_id': '$created.user',
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$group': {
            '_id': '$count',
            'num_users': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            '_id': 1
        }
    }, {
        '$limit': 1
    }]

def most_common_buildings():
    """
    returns top 10 building types
    """
    return [{
        '$match': {
            'building': {
                '$exists': 1
            }
        }
    }, {
        '$group': {
            '_id': '$building',
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    }, {
        '$limit': 10
    }]

def top_amenities():
    '''
    returns top 5 amenities
    '''
    return [{
        '$match': {
            'amenity': {
                '$exists': 1
            } 
        } 
    }, {
        '$group': {
            '_id': '$amenity', 
            'count': {
                '$sum':1
            } 
        } 
    }, {
        '$sort': {
            'count':-1
        }
    }, {
        '$limit': 5
    }]

def top_cafe():
    '''
    returns top 3 cafe
    '''
    return [{
        '$match': {
            'amenity': 
                'cafe'
        } 
    }, {
        '$group': {
            '_id': '$name', 
            'count': {
                '$sum':1
            } 
        } 
    }, {
        '$sort': {
            'count':-1
        }
    }, {
        '$limit': 3
    }]

def top_fast_food():
    '''
    returns top 2 fast food
    '''
    return [{
        '$match': {
            'amenity': {
                '$exists': 1
            }, 
            'amenity': 
                'fast_food'
        }
    }, {
        '$group': {
            '_id': '$name', 
            'count': {
                '$sum':1
            } 
        } 
    }, {
        '$sort': {
            'count':-1
        }
    }, {
        '$limit': 2
    }]

if __name__ == '__main__':
    db = get_db()
    print "top contributing user"
    pprint(list( db.openstreetmap.aggregate(top_user()) ))
    raw_input("Press enter to continue...\n")

    print "number of single contributing users"
    pprint(list( db.openstreetmap.aggregate(single_post_users()) ))
    raw_input("Press enter to continue...\n")

    print "most common buildings"
    pprint(list( db.openstreetmap.aggregate(most_common_buildings()) ))
    raw_input("Press enter to continue...\n")

    print "most common amenities"
    pprint(list( db.openstreetmap.aggregate(top_amenities()) ))
    raw_input("Press enter to continue...\n")

    print "top 3 cafe"
    pprint(list( db.openstreetmap.aggregate(top_cafe()) ))
    raw_input("Press enter to continue...\n")

    print "top 2 fast food"
    pprint(list( db.openstreetmap.aggregate(top_fast_food()) ))
    raw_input("Press enter to continue...\n")