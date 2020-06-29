import json
import py2neo
from py2neo import Graph
import config as conf
import csv
import shutil, os
from pathlib import Path

uri = "{}://{}:{}@{}:{}".format(conf.PROTO, conf.USER, conf.PASSWORD, conf.HOSTNAME, conf.PORT)

graph = Graph(uri)
matcher = py2neo.NodeMatcher(graph) 

def select_business(state="AZ",cat='Restaurants'):
    bus_dict = graph.run("MATCH (business:Business)-[:IN_CATEGORY]->(c:Category) WHERE c.id in $categories RETURN business",parameters={'categories':cat}).data() 
    #bu = result[0]['business']['name']
    #Get a list of all bussiness using 'where' statement with the regex .*
    #bus_list= list(matcher.match("Business").where("_.name =~ '.*'"))
    bus_selected = [dict() for x in range(1)]
    for bus in bus_dict:
        if(bus['business']['state']==state):
            bus_selected.append(bus['business'])
    bus_selected.pop(0)
    return bus_selected
def clean_data():
    folder = Path("./")
    file = folder / "photo.json"
    with open(file) as f:
         # Import json data into an array of json objects
        data = [json.loads(line) for line in f] 
    dictlist = [dict() for x in range(1)]
    for d in data:
        #Filter out photos with non food labels and no captions
        #if((d['label']=='food') and (d['caption'] != "")):
        if(d['label']=='food'):
            dictlist.append(d)
    dictlist.pop(0)
    return dictlist
def extract_photos(dictlist=dict(), business="all"):
    extract = [dict() for x in range(1)]
    for d in dictlist:
        if((d['business_id']==business) or (business =="all")):
            #print(d)
            extract.append(d)
    extract.pop(0)
    return extract
def Arizona_photo_set():
    cat_folder = Path("./")
    food_category_file = cat_folder / "foodrelated_categories.txt"
    category_list = [line.rstrip('\n') for line in open(food_category_file)]
    select = select_business(state="AZ",cat=category_list)
    e_ret = [dict() for x in range(1)]
    clean_dictionary = clean_data()
    for s in select:
        e_temp = extract_photos(dictlist=clean_dictionary,business=s['id']) 
        if(e_temp != []):
            for ex in e_temp:
                e_ret.append(ex)
    e_ret.pop(0)
    return e_ret

def copy_photos():
    pics = [] 
    #Example of a business id
    #business_id = "6nKR80xEGHYf2UxAe_Cu_g"
    yset = Arizona_photo_set()
    for y in yset:
        #Uncomment the following if statemnt to select a specific
        #business
        #if(y['business_id'] == business_id): 
            #pics.append(y['photo_id'])
            photo_folder = Path("./photos/")
            temp_folder = Path('./temp')
            #shutil.copy(photo_file, temp_folder)
            shutil.copy(os.path.join(photo_folder,str(y['photo_id'])+'.jpg'),temp_folder)
