import json
import sqlite3
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Turns the a list of jsons nad the vendor order into a easly insertable 
#   list for the db
#
# Note: some class items and stuff dont have collectable hash
#   so idk how to fix that, ill do it later
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def CollectafyData(JSONLIST, vendorORDER):
    collectionList = []
    counter = 0
    for response in JSONLIST:
        for sales in response["Response"]["sales"]["data"]:
            hash = response['Response']['sales']['data'][sales]['itemHash']
            if (hash > 2147483647):
                hash = hash - 4294967296
            try:
                # if response['Response']['sales']['data'][sales]['costs'][0] != 3147280338:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                con = sqlite3.connect(dir_path + '/manifest.db')
                cur = con.cursor()
                query = f"SELECT json \
                    from DestinyInventoryItemDefinition \
                    WHERE id = {hash}"
                cur.execute(query)
                item = json.loads(cur.fetchall()[0][0])
                try:
                    collectionID = item["collectibleHash"]
                    collectionTuple = (item['displayProperties']['name'], collectionID, vendorORDER[counter])
                    collectionList.append(collectionTuple)
                except:
                    pass
            except: 
                pass
        counter = counter + 1

    res = []
    [res.append(x) for x in collectionList if x not in res]
    collectionList = res
    return collectionList


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# add the input list of collectables, their hashes, and vendor into the db
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def AddSalesToDB(list):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    con = sqlite3.connect(dir_path + '/MYDB.db')
    cur = con.cursor()
    query = 'DROP TABLE IF EXISTS CurrentSales'
    cur.execute(query)
    query = 'create table CurrentSales (Name, CollectionHash, Vendor)'
    cur.execute(query)
    for index in list:
        query = f"INSERT INTO CurrentSales (Name, CollectionHash, Vendor)\
                    VALUES {index[0], index[1], index[2]};"
        cur.execute(query)
        con.commit()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# reads the info from the database
#
# returns a list of tuples for all collectableSales
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def readAllSales():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    con = sqlite3.connect(dir_path + '/MYDB.db')
    cur = con.cursor()
    query = 'SELECT * FROM CurrentSales'
    cur.execute(query)
    allSales = cur.fetchall()
    cur.close()
    return allSales

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# compares a tuple list of current sales with a players collectibles
#
# returns a tuple list of missing items
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

vendorEnumShifts = {
        "Xûr": 0,
        "Ada-1": 1,
        "Tess Everis": 2,
        "Banshee-44": 3,
    }
def checkMissingCollectables(CurrentSales, collectiblesJSON, checkEnums):
    UserMissing = []
    for item in CurrentSales:
        collectionVal = 0
        try:
            collectionVal = collectiblesJSON["profileCollectibles"]["data"]["collectibles"][f"{item[1]}"]["state"]
            collectionVal = collectionVal & 0x1
            # print(f"    item: {item[0]} has a state of: {collectionVal}")
        except:
            charecterCollection = collectiblesJSON["characterCollectibles"]["data"]
            for thing in charecterCollection:
                try:
                    collectionVal = charecterCollection[thing]["collectibles"][f"{item[1]}"]["state"]
                    collectionVal = collectionVal & 0x1
                    # print(f"    item: {item[0]} has a state of: {collectionVal} for vendro {item[2]}")
                    break
                except:
                    print(f"    Error finding the item {item[0]} with hash {item[1]} for vendro {item[2]}")
                    pass
            pass        
        finally:
            # used the enum maping to see if the user has selected to recive texts for the vendor
            if (collectionVal == 1):
                if((int(checkEnums) >> vendorEnumShifts[item[2]] & 0x1) == 1):
                        UserMissing.append(item)
                else:
                    if((int(checkEnums) >> 8 & 0x1) == 1):
                        UserMissing.append(item)
                   
    return UserMissing


    
    # ENUMS
# 1 Xur for friday
# 2 Ada-1
# 4 Tess
# 8 Banshee-44
# 16  --Place Holder --
# 32  --Place Holder --
# 64  --Place Holder --
# 128 --Place Holder --
# 256 Everyone