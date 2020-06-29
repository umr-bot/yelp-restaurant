## To use this file the full set of businesses business.json should
## contained in the same directory as this python file

import json

def generate_business_subset(size=2000):
    with open('business.json','r') as f:
        b_data = [json.loads(line) for line in f]
    
    az_data = []
    # Select only businesses in the state Arizona 
    for b in b_data:
        if(b['state'] == 'AZ'):
            az_data.append(b)
    return az_data[0:size]

def write_data_to_file(data,filename='business_subset_0.01.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
