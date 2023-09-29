import base64
import requests
import json
import sys
from requests_oauthlib import OAuth2Session


# vendor Hashes
VendorList = [

                # Usable Charecters
                 ["Xûr", "2190858386"]
                ,["Banshee-44", "672118013"]
                ,["Ada-1", "350061650"]
                # ,["Tess Everis", "3361454721"]

                # # Weekend
                # ["Xûr", "2190858386"],
                # # Helm
                # ["War Table", "4287814313"], ["Crown of Sorrow", "2748388973"], ["Star Chart", "518338309"] , ["Exo Frame", "1043079869"],
                # # Witch Queen
                # ["Fynch", "2384113223"], ["Relic Conduit","3642056527"],
                # # 30th
                # ["Xûr 30th", "3442679730"], ["Starhorse", "3431983428"],
                # # Tower
                # ["Suraya Hawthorne", "3347378076"], ["Commander Zavala", "69482069"]  , ["Ikora Rey", "1976548992"], ["Lord Shaxx", "3603221665"],
                # ["Master Rahool", "2255782930"], ["Banshee-44", "672118013"], ["Amanda Holliday", "460529231"], ["The Drifter", "248695599"],
                # ["Saint-14", "765357505"], ["Quest Archive", "3484140575"], ["Monument to Lost Lights", "4230408743"], ["Ada-1", "350061650"],    
                # # World
                # ["Devrim Kay", "396892126"], ["Failsafe", "1576276905"],["Petra Venj", "1841717884"] ,["Eris Morn", "1616085565"], 
                # ["Lectern of Enchantment", "3411552308"], ["Variks the Loyal", "2531198101"], ["Shaw Han", "1816541247"]
            ]

# fuck it i might just have the follwoing vendors available:
# Ada-1
# Tess
# Banshee-44

# test so i dont have to wait a long time if i want to see just one vendor 
# VendorList = [["Fynch", "2384113223"]]
            # this is tess and she is messed up 
# Friday Specal
# 0:2190858386 // <Vendor "Xûr">

# Helm
# 0:4287814313 // <Vendor "War Table">
# 1:2748388973 // <Vendor "Crown of Sorrow">
# 2:518338309 // <Vendor "Star Chart">
# 3:1043079869 // <Vendor "Exo Frame"> 

# witch Queen
# 0:2384113223 // <Vendor "Fynch">
# 1:3642056527 // <Vendor "Relic Conduit">

# 30th
# 0:3442679730 // <Vendor "Xûr">
# 1:3431983428 // <Vendor "Starhorse">

# Tower
# 0:3347378076 // <Vendor "Suraya Hawthorne">
# 1:69482069 // <Vendor "Commander Zavala">
# 2:1976548992 // <Vendor "Ikora Rey">
# 3:3603221665 // <Vendor "Lord Shaxx">
# 4:2255782930 // <Vendor "Master Rahool">
# 5:672118013 // <Vendor "Banshee-44">
# 6:460529231 // <Vendor "Amanda Holliday">
# 7:248695599 // <Vendor "The Drifter">
# 8:765357505 // <Vendor "Saint-14">
# 9:3484140575 // <Vendor "Quest Archive">
# 10:4230408743 // <Vendor "Monument to Lost Lights">
# 11:350061650 // <Vendor "Ada-1">
# 12:3361454721 // <Vendor "Tess Everis">

# Planets
# 0:396892126 // <Vendor "Devrim Kay">
# 1:1576276905 // <Vendor "Failsafe">
# 2:1841717884 // <Vendor "Petra Venj">
# 3:1616085565 // <Vendor "Eris Morn">
# 4:3411552308 // <Vendor "Lectern of Enchantment">
# 5:2531198101 // <Vendor "Variks the Loyal">
# 6:1816541247 // <Vendor "Shaw Han">




# Hashes to remember
# Charecter type Hashes
# Warlock: 2271682572 
# Hunter: 671679327 
# Titan: 3655393761


# for getting the info for the wesite the following url is to be used
# /Platform/Destiny2/{Membershiptype}/Profile/{MembershipID}/?components=200



 # get the stored info 
infoFile = open('info.json', 'r')
dataJSON = json.load(infoFile)
infoFile.close()

api_key = dataJSON["X-API-Key"]
client_id = dataJSON["client_id"]
client_secret = dataJSON["client_secret"]
refresh_token = dataJSON["refresh_token"]
redirect_url = dataJSON["redirect_url"]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# fetch the data from bungie and save it into my own local db if its a collectable
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def fetchAllSales(HEADERS):
    # These are my chars put in env 
    charecterIDS = ["2305843009265217409", "2305843009701865527", "2305843009265217408"]
    myID = 4611686018434521900
    num = 0
    vendorORDER = []
    JSONLIST = []
    for hash in VendorList:
        count = 1
        for character in charecterIDS:
            user_details_endpoint = f"https://www.bungie.net/Platform/Destiny2/2/Profile/{myID}/Character/{character}/Vendors/{hash[1]}/?components=402"
            response = requests.get(url=user_details_endpoint, headers = HEADERS)
            errorcode = json.loads(response.text)["ErrorCode"]
            if (errorcode == 1):
                JSONLIST.append(json.loads(response.text))
                vendorORDER.append(hash[0])
            elif (errorcode == 1688):
                while (errorcode == 1688):
                    if(errorcode == 1688):
                        print("trying again")
                    user_details_endpoint = f"https://www.bungie.net/Platform/Destiny2/2/Profile/{myID}/Character/{character}/Vendors/{hash[1]}/?components=402"
                    response = requests.get(url=user_details_endpoint, headers = HEADERS)
                    errorcode = json.loads(response.text)["ErrorCode"]
                JSONLIST.append(json.loads(response.text))
                vendorORDER.append(hash[0])
            else:
                print(f"failed on: {hash[0]} using Character: {character}")
                print(response.text)
            num = num + 1
            precent = num / (len(VendorList) * 3 )* 100
            sys.stdout.write(f"\r({precent:0.2f}%) {hash[0]} ({count}/3)")
            count = count + 1
            if (count == 4):
                print()
    return [JSONLIST, vendorORDER]
    


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# uses the refesh token so i can use any command
# 
# returns the header thats to be used with every request
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def updateToken():

    # Oauth Shit, probably could use a better library but it works
    base64_encoded_clientid_clientsecret = base64.b64encode(str.encode(f'{client_id}:{client_secret}'))  # concatenate with : and encode in base64
    base64_encoded_clientid_clientsecret = base64_encoded_clientid_clientsecret.decode('ascii')  # turn bytes object into ascii string
    url = "https://www.bungie.net/Platform/App/OAuth/token/"
    headers = {
        'X-API-Key': api_key,
        'Authorization': f'Basic {base64_encoded_clientid_clientsecret}'
        }
    data = {
        "headers":headers, 
        "grant_type":"refresh_token", 
        "refresh_token":refresh_token
    }

    # Deal with the response
    response = requests.post(url, headers=headers, data = data)
    jsonResponse = json.loads(response.text)
    if ("error" in jsonResponse):
        print(f"unsuccessfull (token is probably wrong or expired) {jsonResponse}")
        return None
    newRefresh_token = jsonResponse["refresh_token"]
    usable_token = jsonResponse["access_token"]

    dataJSON["refresh_token"] = newRefresh_token
    infoFile = open('info.json', 'w')
    json.dump(dataJSON, infoFile, indent=4)
    infoFile.close()

    # reuturn in the foramt of the HEADER
    return {"X-API-Key":api_key, "Authorization": f"Bearer {usable_token}"}

def manualOauth():
    base_auth_url = "https://www.bungie.net/en/OAuth/Authorize"
    token_url = "https://www.bungie.net/platform/app/oauth/token/"

    session = OAuth2Session(client_id=client_id, redirect_uri=redirect_url)

    auth_link = session.authorization_url(base_auth_url)
    print(f"Authorization link: {auth_link[0]}")

    redirect_response = input(f"Paste url link here: ")

    response = session.fetch_token(
        client_id=client_id,
        client_secret=client_secret,
        token_url=token_url,
        authorization_response=redirect_response
    )
    refresh_token = response["refresh_token"]

    dataJSON["refresh_token"] = refresh_token
    infoFile = open('info.json', 'w')
    json.dump(dataJSON, infoFile, indent=4)
    infoFile.close()
    return
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# fetched the a players collection given their membershipId and a vaild header for request
# 
# returns the collection as a json
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def fetchPlayerCollection(membershipId, HEADERS):
    print("---fetching colletions---")
    for type in range (4):
        print(f"trying type: {type}")
        user_details_endpoint = f"https://www.bungie.net/Platform/Destiny2/{type}/Profile/{membershipId}/?components=Collectibles"
        response = requests.get(url=user_details_endpoint, headers = HEADERS)
        if(json.loads(response.text)["ErrorCode"] == 1):
            print(f"Success on type: {type}")
            break

    collectiblesJSON = json.loads(response.text)["Response"]
    print("---fecthing DONE---")
    return collectiblesJSON


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# uses the refesh token so i can use any command
# 
# returns the players membership ID
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def ValidatePlayer(name, code, HEADERS):
    # given a user input check to see if a player existes and return the membershipID
    myobj = {"displayName": name, "displayNameCode": code}
    user_details_endpoint = "https://www.bungie.net/Platform//Destiny2/SearchDestinyPlayerByBungieName/-1/"
    resonse = requests.post(url =user_details_endpoint, json =myobj, headers = HEADERS)
    try:
        membershipId = json.loads(resonse.text)["Response"][0]["membershipId"]
    except:
        print(f"User {name}#{code} is not valid")
        exit()
    return membershipId

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# add the input list of collectables, their hashes, and vendor into the db
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# def AddSalesToDB(list):
#     con = sqlite3.connect('Sales.db')
#     cur = con.cursor()
#     query = 'DROP TABLE IF EXISTS CurrentSales'
#     cur.execute(query)
#     query = 'create table CurrentSales (Name, CollectionHash, Vendor)'
#     cur.execute(query)
#     for index in list:
#         query = f"INSERT INTO CurrentSales (Name, CollectionHash, Vendor)\
#                     VALUES {index[0], index[1], index[2]};"
#         cur.execute(query)
#         con.commit()

# check to see if 1660918514  maps to 1660918514 
# or see if i can get json and find 