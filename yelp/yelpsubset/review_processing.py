from yelp.yelpsubset.user_data_processing import *
from yelp.yelpsubset.business_subset_generator_v2 import *

def get_5_top_star_bus(user,city,category):
    p_sub = Path('yelp/yelpsubset/')
    my_file1 = p_sub / 'user_subset_001.json'
    with open(my_file1,'r') as f:
        user_data = [json.loads(line) for line in f]
    p_sub = Path('yelp/yelpsubset/')
    my_file2 = p_sub / 'business_subset_001.json'
    with open(my_file2,'r') as f:
        bus_data = [json.loads(line) for line in f]
     
    my_users = get_user_friends_of_friends(user,user_data)
    rev_path = Path('yelp/yelpsubset/')/'reviews_subset_0.01.json'
    revs = read_from_file(bus=rev_path,size=7531) 
    buss = []
    for rev in revs:
        if(rev['user_id'] in my_users):
            buss.append(rev['business_id'])
    if buss == [] : return []
    buss_objects = []
    for buss_name in buss:
        buss_objects.append(get_business(bus=buss_name,data=bus_data))
    ret_bus = []
    for bus_object in buss_objects:
        ## Check if same category and city
        #Clean category data of white spaces
        cleaned_cat = [x.strip(' ') for x in bus_object['categories']]
        if bus_object['city'] == city and category in cleaned_cat:
            ret_bus.append(bus_object)
    sorted(ret_bus, key=lambda k: k['stars'],reverse=True)
    
    return ret_bus[0:5]
# Get business object from business_subset_001.json
# bus is business_id of the requested business and data is all objects
# in business_subset__001.json
def get_business(bus,data):
    for b in data:
        if(b['business_id'] == bus):
            return b
    return []
