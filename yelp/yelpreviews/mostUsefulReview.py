#Created by: James Winston Mercuur - 18995543

# Imports
from py2neo import Graph
from . import config
import datetime as dt

# Setup the graphing tool and access to the database
uri = "{}://{}:{}@{}:{}".format(config.PROTO, config.USER, config.PASSWORD, config.HOSTNAME, config.PORT)
graph = Graph(uri)

# Get the reviews for the selected restaurant using a default restaurant at the moment to make sure it works
def getReviews(busi_id = "gnKjwL_1w79qoiV3IC_xQQ"):    
    # The only flag I will ever need
    noReviews = 0
    
    # Get the date today two years ago
    tday = dt.datetime.today()
    dateTwoYearsAgo = str(dt.datetime((tday.year - 2), tday.month, tday.day, tday.hour, tday.minute, tday.second))
    
    # Cypher code to get the reviews
    review_dict = graph.run("""MATCH (u:User)-[r:REVIEWS]->(b:Business) 
                            WHERE b.id = \"""" + busi_id + """\" AND r.date >= \"""" + dateTwoYearsAgo + """\" 
                            RETURN u.name, u.stars, r.useful, r.text, r.date 
                            ORDER BY r.useful DESC, r.date DESC""").data()
                            
    # The design decision to handle no reviews in the last two years
    if len(review_dict) == 0:
        review_dict = graph.run("""MATCH (u:User)-[r:REVIEWS]->(b:Business) 
                                WHERE b.id = \"""" + busi_id + """\" 
                                RETURN u.name, u.stars, r.useful, r.text, r.date 
                                ORDER BY r.useful DESC, r.date DESC""").data()
                                
        if len(review_dict) == 0:
            noReviews = 1
                            
    return review_dict, noReviews

# Get the most usefull review from the dictionary of reviews
def getMostUsefulReview(reviews):
    mostUsefulRev = dict()
    for x in range(len(reviews)):
        if reviews[x]["r.useful"] != None:
            mostUsefulRev = reviews[x]
            break;
        
    return mostUsefulRev

# Return the name of the reviewer and their rating
def getNameAndStars(mostUsefulReview):
    name = mostUsefulReview["u.name"]
    stars = mostUsefulReview["u.stars"]
    
    if stars == None:
        stars = 0
    
    return str(name), str(stars)

# Display the info on the webpage
def displayInfo(name, stars, review):
    
    return [str(name), str(stars), "\"" + str(review) + "\""]

# Main function duh
def mainFunc(businessID = "GWO87Y-IqL54_Ijx6hTYAQ"):
        
    reviews, noReviews = getReviews(businessID)
    
    if noReviews != 1:
        mostUsefulReview = getMostUsefulReview(reviews)
    
        name, stars = getNameAndStars(mostUsefulReview)
    
        RESULTS = displayInfo(name, stars, mostUsefulReview["r.text"])
        
    elif noReviews == 1:
        
        RESULTS = displayInfo("THARUN", "WE DONT HAVE", "ANY REVIEWS")
    
    return RESULTS