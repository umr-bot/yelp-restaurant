import datetime as dt
from flask import Flask, render_template, request, url_for, flash, redirect
from .forms import *
from .input import *
import json
from pathlib import Path
#from yelp.yelpphotos import extract_photos_with_food_label as food
import shutil, os
from yelp.yelpsubset import review_processing as rp

from .yelpreviews import mostUsefulReview as MUR
from .Name import getID

## GLOBAL variables
global_category = ""
global_city = ""

app = Flask(__name__, static_url_path='',
            static_folder="static", template_folder='templates')
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

def timeconvert(str1): 
   if str1[-2:] == "AM" and str1[:2] == "12": 
      return "00" + str1[2:-3] 
   elif str1[-2:] == "AM": 
      return str1[:-3] 
   elif str1[-2:] == "PM" and str1[:2] == "12": 
      return str1[:-3] 
   else: 
      return str(int(str1[:2]) + 12) + str1[2:5] 

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

#def is_location(str1):
#   for item in data:
#        if str1 == item['city']:
#            return True    
#    return False

s = dt.datetime.strptime('12:00 AM', '%I:%M %p') #code to get a list of times that increment by 30min with am,pm etc
r = []
r.append(s.strftime('%I:%M %p'))
for i in range(30,60*24,30):
    r.append((s+dt.timedelta(minutes=i)).strftime('%I:%M %p'))

#extracting info from subset.json
#folder = Path("yelp-subset")
#file_to_open = folder / "business_subset_0.02.json"
#with open('/Users/lizanebotha/Documents/ENGINEERING/WebDevelopment/Project2/group1-rw334/src/yelp-subset/business_subset_0.01.json', 'r') as json_file:
#with open(file_to_open, 'r') as json_file:
#    data = [json.loads(line) for line in json_file]

#selectors data
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
categories = ['Pizza','Italian','Burger','Chinese','Thai','Japanese','Mexican']
cuisines = ['American (New)', 'American (Traditional)', 'Asian Fusion', 'Bagels', 'Bakeries', 'Barbeque', 'Burgers', 'Chicken Wings', 'Chinese', 'Ethnic Food', 'Fast Food', 'French', 'Gluten-Free', 'Halal', 'Hawaiian', 'Indian', 'Italian', 'Japanese', 'Juice Bars & Smoothies', 'Latin American', 'Local Flavor', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Pizza', 'Poke', 'Ramen', 'Salad', 'Sandwiches', 'Seafood', 'Soup', 'Specialty Food', 'Steakhouses', 'Sushi Bars', 'Tacos', 'Tapas/Small Plates', 'Tex-Mex', 'Vietnamese', 'Wraps']
#cuisines specifically from the different types in state:AZ
times = r
locations = ['Avondale', 'Cave Creek', 'Chandler', 'Fountain Hills', 'Gilbert', 'Glendale', 'Goodyear', 'Mesa', 'Paradise Valley', 'Peoria', 'Phoenix', 'Scottsdale', 'Sun City', 'Surprise', 'Tempe']

#data is the business_subset_0.01.json
"""format: 
    {"business_id": "1SWheh84yJXfytovILXOAQ", "name": "Arizona Biltmore Golf Club", 
    "address": "2818 E Camino Acequia Drive", "city": "Phoenix", "state": "AZ", 
    "postal_code": "85016", "latitude": 33.5221425, "longitude": -112.0184807, 
    "stars": 3.0, "categories": ["Golf", "Active Life"], "is_open": false}
"""

@app.route('/', methods=['GET','POST'])
@app.route('/user_input', methods=['GET','POST'])
def user_input():
    form=userInputForm()

    if request.method=='POST':#submit button pushed
        day = request.form.get('days')
        category = request.form.get('categories')
        location = request.form.get('locations')
        time = timeconvert(request.form.get('times'))
        print(day,category,time,location)
        #my_list = rp.get_5_top_star_bus(user='4XChL029mKr5hydo79Ljxg',city=location,category=category)
        ## Using temporary category and city to fix results temporarily
        top5bus = rp.get_5_top_star_bus(user='4XChL029mKr5hydo79Ljxg',city='Scottsdale',category='Bars')
        business_id = getID("'"+location+"'", "'Restaurant'", day, time, time[0:1], time[3:4])
        review_list = MUR.mainFunc(business_id)
        #review_list = MUR.mainFunc()
        #print(my_list)
        return render_template('results.html',
                title='Results',day=day,category=category,location=location,time=time,top5bus=top5bus,review_list=review_list,business_id=business_id)

    return render_template('user_input.html' , title='Search',days=days, times=times, categories=cuisines, locations=locations, form=form)

@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/help')
def help():
    return render_template('help.html', title='Help')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/results')
def results():
    return render_template('results.html',
            title='Results',day=day,category=category,location=location,
            time=time)

def user_results():    
    day = request.form.get('days')
    category = request.form.get('categories')
    location = request.form.get('locations')
    time = timeconvert(request.form.get('times'))
    print(day,category,time,location)        
    return render_template('results.html',
            title='Results',day=day,category=category,location=location,
            time=time)

    #return render_template('user_input.html' , days=days, times=times,categories=cuisines, locations=locations, form=form)

@app.route('/food_slideshow', methods=["GET", "POST"])
def slideshow(business_id="9vub2LM7Djy8P-LPumcLXA"):
    #images = os.listdir(os.path.join(app.static_folder, "photos"))
    folder = Path('yelp/yelpphotos/')
    my_file = folder / 'Arizona_photo_dataset.json'
    with open(my_file, 'r') as f:
        pdat = [json.loads(line) for line in f]
    images = []
    for i in pdat[0]:
        if(i['business_id'] == business_id):
            images.append(i)
    if(len(images) == 0):
        return render_template('no_images_found.html')
    return render_template('food_slideshow.html', images=images)
