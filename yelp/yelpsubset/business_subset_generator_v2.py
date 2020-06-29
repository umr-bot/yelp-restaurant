import json
from pathlib import Path
## User must place yelp file business.json in this folder themselves as it
## was too large to upload to the repositry

def get_arizona_food_bus(file_name='business.json'):
    
    with open(file_name,'r') as f: 
        b_data = [json.loads(line) for line in f]

    # Filter out only businesses in the state Arizona
    AZ_b_data = []
    for bc in b_data:
        if(bc['state'] == 'AZ'):
            AZ_b_data.append(bc)
    ## Use Path to accommodate for Windows, Linux and MAC OS
    cat_folder = Path("./")
    food_category_file = cat_folder / "foodrelated_categories.txt"
    category_list = [line.rstrip('\n') for line in open(food_category_file)]

    az_food_bus = []
    for a in AZ_b_data: 
            if(a['categories'] != None): 
                contains_category = any(item in a['categories'] for item in category_list) 
                if(contains_category): 
                    az_food_bus.append(a)

    

    return az_food_bus

def write_to_file(data,out_file='business_subset_005.json', size=2000):

    with open(out_file,'w') as f: 
            i = 0 
            for bb in data: 
                if(i >= size): 
                    break 
                f.write(json.dumps(bb)) 
                f.write('\n') 
                i+=1
def read_from_file(bus='user_subset_003.json', size=5000):
    
    with open(bus,'r') as f: 
            i = 0 
            data = []
            for line in f: 
                if(i >= size): 
                    break
                data.append(json.loads(line))
                i+=1
    return data

