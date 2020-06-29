import json
import py2neo
from py2neo import Graph
#from .views import *
parameters= {}

# functions returning necessary business properties
def getName(city,category,day,time,hourstr,minstr):
    return (NameMain(city,category,day,time,hourstr,minstr)[0])

def getID(city,category,day,time,hourstr,minstr):
    return (NameMain(city,category,day,time,hourstr,minstr)[3])

def getAddress(city,category,day,time,hourstr,minstr):
    return (NameMain(city,category,day,time,hourstr,minstr)[1])


def getStars(city,category,day,time,hourstr,minstr):
    return (NameMain(city,category,day,time,hourstr,minstr)[2])


def getCount(city,category,day,time,hourstr,minstr):
    return (NameMain(city,category,day,time,hourstr,minstr)[4])


# function to return the index of correct business to user
def getIndex(numelements, listday, hourstr):
    # If no businesses are found
    for k in range(numelements):
        if (k == numelements - 1) and (listday[k][0] == 'o'):
            return (-10)

        if listday[k][0] != 'o':
            sep1index = 0
            temphyph = 0
            sep2index = 0
            temp1hour = ''
            temp2hour = ''
            templength = len(listday[k])

            for t in listday[k]:
                if t == '-':
                    listbite1 = ''
                    listbite2 = ''
                    hyphindex = temphyph

                    for j in range(0, hyphindex - 1):
                        listbite1 = listbite1 + listday[k][j]
                    for j in range(hyphindex + 1, templength):
                        listbite2 = listbite2 + listday[k][j]

                    for u in listbite1:
                        if (len(temp1hour) != 2) and (u != ':'):
                            temp1hour = temp1hour + listbite1[sep1index]
                            sep1index += 1
                    for u in listbite2:
                        if (len(temp2hour) != 2) and (u != ':'):
                            temp2hour = temp2hour + listbite2[sep2index]
                            sep2index += 1

                    if (temp1hour[0] == '0'):
                        temp1hour = '0'
                    if (temp2hour[0] == '0'):
                        temp2hour = '24'
                    if (listbite1[len(listbite1) - 1] == '3') or (listbite1[len(listbite1) - 2] == '3'):
                        temp1hour = temp1hour + '.5'
                    if (listbite2[len(listbite2) - 1] == '3') or (listbite2[len(listbite2) - 2] == '3'):
                        temp2hour = temp2hour + '.5'

                    if (float(hourstr) > float(temp1hour) or float(hourstr) == float(temp1hour)) and float(
                            hourstr) < float(temp2hour):
                        return k
                    else:
                        if (k==numelements-1):
                            return (-10)
                temphyph += 1

def GetParam(getcity,getcategory,getday,gettime):
    # input parameters
    city = getcity
    category = getcategory
    day = getday
    time = gettime
    # separating time into minutes and hours
    hourstr = time[0] + time[1]
    minstr = time[3] + time[4]
    parameters[0]="'"+city+"'"
    parameters[1]="'"+category+"'"
    parameters[2]=day
    parameters[3]=time
    parameters[4]=hourstr
    parameters[5]=minstr

    return ()
def NameMain(city,category,day,time,hourstr,minstr):
    # accessing graph
    uri = "bolt://neo4j:1532@localhost:8000"
    numelements = 0
    graph = Graph(uri)
    matcher = py2neo.NodeMatcher(graph)
    busindex = 0

    # adding concession for half hours
    if minstr[0] == '3':
        hourstr = hourstr + '.5'

    # fetching from graph
    namecom = "MATCH (n:Business)-[:IN_CATEGORY]->(c:Category) WHERE (c.id=" + category + ") AND (n.state='AZ') AND (n.city=" + city + ") RETURN (n.name) ORDER BY n.stars desc,n.review_count desc"
    daycom = "MATCH (n:Business)-[:IN_CATEGORY]->(c:Category) WHERE (c.id=" + category + ") AND (n.state='AZ') AND (n.city=" + city + ") RETURN (n." + day + ") ORDER BY n.stars desc,n.review_count desc"
    addresscom = "MATCH (n:Business)-[:IN_CATEGORY]->(c:Category) WHERE (c.id=" + category + ") AND (n.state='AZ') AND (n.city=" + city + ") RETURN (n.address) ORDER BY n.stars desc,n.review_count desc"
    idcom = "MATCH (n:Business)-[:IN_CATEGORY]->(c:Category) WHERE (c.id=" + category + ") AND (n.state='AZ') AND (n.city=" + city + ")  RETURN (n.id) ORDER BY n.stars desc,n.review_count desc"
    starcom = "MATCH (n:Business)-[:IN_CATEGORY]->(c:Category) WHERE (c.id=" + category + ") AND (n.state='AZ') AND (n.city=" + city + ")  RETURN (n.stars) ORDER BY n.stars desc,n.review_count desc"
    countcom = "MATCH (n:Business)-[:IN_CATEGORY]->(c:Category) WHERE (c.id=" + category + ") AND (n.state='AZ') AND (n.city=" + city + ")  RETURN (n.review_count) ORDER BY n.stars desc,n.review_count desc"

    # converting from cursor object to a string object
    namestring = (graph.run(namecom)).data()
    daystring = (graph.run(daycom)).data()
    addressstring = (graph.run(addresscom)).data()
    idstring = (graph.run(idcom)).data()
    starstring = (graph.run(starcom)).data()
    countstring = (graph.run(countcom)).data()

    # to be filled with final sorted, relevant properties (final list)
    listname = {}
    listaddress = {}
    listday = {}
    listid = {}
    liststars = {}
    listcount = {}

    # temporary list used to update final lists
    tempname = {}
    tempid = {}
    tempday = {}
    tempaddress = {}
    tempstars = {}
    tempcount = {}

    # getting total number of elements
    for t in namestring:
        numelements += 1
    if (numelements < 1):
        return ("No restaurants found that match your criteria", "", "", "", "")

    # filling list with necessary string elements
    for x in range(numelements):
        tempname[x] = str(namestring[x])
        tempaddress[x] = str(addressstring[x])
        tempday[x] = str(daystring[x])
        tempid[x] = str(idstring[x])
        tempstars[x] = str(starstring[x])
        tempcount[x] = str(countstring[x])
    for x in range(numelements):

        lengthname = len(tempname[x])
        lengthaddress = len(tempaddress[x])
        lengthopen = len(tempday[x])
        lengthid = len(tempid[x])
        lengthstars = len(tempstars[x])
        lengthcount = len(tempcount[x])

        wordname = ''
        wordaddress = ''
        wordday = ''
        wordid = ''
        wordstars = ''
        wordcount = ''

        # Handling inconsistincies in dataset for days
        if (day == "Monday") or (day == "Sunday") or (day == "Friday"):
            for k in range(16, lengthopen - 2):
                wordday = wordday + str(tempday[x][k])
            listday[x] = wordday
        if (day == "Saturday") or (day == "Thursday"):
            for k in range(18, lengthopen - 2):
                wordday = wordday + str(tempday[x][k])
            listday[x] = wordday
        if (day == "Tuesday"):
            for k in range(18, lengthopen - 2):
                wordday = wordday + str(tempday[x][k])
            listday[x] = wordday
        if (day == "Wednesday"):
            for k in range(19, lengthopen - 2):
                wordday = wordday + str(tempday[x][k])
            listday[x] = wordday

        # filling lists
        for k in range(14, lengthname - 2):
            wordname = wordname + str(tempname[x][k])
        listname[x] = wordname
        for k in range(18, lengthaddress - 2):
            wordaddress = wordaddress + str(tempaddress[x][k])
        listaddress[x] = wordaddress
        for k in range(12, lengthid - 2):
            wordid = wordid + str(tempid[x][k])
        listid[x] = wordid
        for k in range(14, lengthstars - 3):
            wordstars = wordstars + str(tempstars[x][k])
        liststars[x] = wordstars
        for k in range(21, lengthcount - 1):
            wordcount = wordcount + str(tempcount[x][k])
        listcount[x] = wordcount

    busindex = getIndex(numelements, listday, hourstr)

    if (busindex == -10):

        return ("No restaurants found that match your criteria", "", "", "", "")
    # display of final relevant properties
    else:

        return (listname[busindex], listaddress[busindex], liststars[busindex], listid[busindex], listcount[busindex])





