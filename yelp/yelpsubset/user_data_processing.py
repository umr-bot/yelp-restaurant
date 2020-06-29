# Gets a list of the user json data
# Input Arguments: user the user_id of requested
#                  data the user.json dataset
# Return a list with the user data
# Returns an empty list of the user_id does not exist
def get_user(user,data):
    for d in data:
    #for i in range(0,len(data)):
        #if(data[i]['user_id'] == user):
        if(d['user_id'] == user):
            #print(data[i])
            return d
    return []
# Gets the friends of the friends of the user
# sorted in descending order
def get_user_friends_of_friends(user,data): 
    my_u = get_user(user=user,data=data)
    if my_u == []: return []
    fofs = []
    for my_f in my_u['friends']: 
        temp_u = get_user(user=my_f,data=data) 
        if(temp_u != []): 
            #print("YAY not empty") 
            fofs.append(temp_u)
    fofs_sort = sorted(fofs, key=lambda k: k['review_count'],reverse=True)
    my_u['friends'].insert(0,my_u['user_id'])
    if fofs_sort == []: return my_u['friends']
    for fr in my_u['friends']:
        fofs_sort.insert(0,fr['friends'])
    
    #Include the user him/herself
    fofs_sort.append(my_u['user_id'])
    return fofs_sort

# Reduce user_subset to containing only three keys:value sets per
# json object namely the user_id, friends and review_count keys
def reduce_subset(data,num_friends = 25):
    ll = []
    for r in data:
        reduced_friends = []
        f_cnt = 0
        #r_split = r['friends'].split(',')
        for r_fri in r['friends']:
            if f_cnt >= num_friends: break
            reduced_friends.append(r_fri)
            f_cnt += 1
        r['friends'] = reduced_friends
        ll.append({'user_id':r['user_id'],
                   'friends':r['friends'],
                   'review_count':r['review_count']
        })
    return ll
## Get all food related businesses in the state Arizona
def reduce_bus_subset(data):
    ll = []
    with open('foodrelated_categories.txt','r') as f:
        fc = f.read().splitlines()
    for r in data:
        if r['categories'] != None:
            if r['state'] != 'AZ' or (not any(item in r['categories'] for item in fc) ): 
                continue
                        
            temp_cat = r['categories'].split(',')
            r['categories'] = temp_cat
            
            if r['hours'] != None:
                #dictList = [{k:v for k,v in zip(r['hours'].keys(), r['hours'].values())}]
                #r['hours'] = dictList

                my_dict = {'business_id':r['business_id'],
                           'name':r['name'],
                           'address':r['address'],
                           'city':r['city'],
                           'state':r['state'],
                           'stars':r['stars'],
                           'review_count':r['review_count'],
                           'categories':r['categories']
                           }
                for day in r['hours']:
                    if day == 'Monday':
                        my_dict.update({'Monday':r['hours']['Monday']})
                    if day == 'Tuesday':
                        my_dict.update({'Tuesday':r['hours']['Tuesday']})
                    if day == 'Wednesday':
                        my_dict.update({'Wednesday':r['hours']['Wednesday']})
                    if day == 'Thursday':
                        my_dict.update({'Thursday':r['hours']['Thursday']})
                    if day == 'Friday':
                        my_dict.update({'Friday':r['hours']['Friday']})
                    if day == 'Saturday':
                        my_dict.update({'Saturday':r['hours']['Saturday']})
                    if day == 'Sunday':
                        my_dict.update({'Sunday':r['hours']['Sunday']})
                ll.append(my_dict)
            else:
                ll.append({'business_id':r['business_id'],
                           'name':r['name'],
                           'address':r['address'],
                           'city':r['city'],
                           'state':r['state'],
                           'stars':r['stars'],
                           'review_count':r['review_count'],
                           'categories':r['categories']
                           })

    return ll

######### TESTING 1,2,3  ##########
#rd = read_from_file(bus='user_subset_001.json',size=50000) 
#my_users = get_user_friends_of_friends(user='bc8C_eETBWL0olvFSJJd0w',data=rd)
