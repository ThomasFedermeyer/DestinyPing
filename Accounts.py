import Bungie_Requests
import mysql.connector
import json

infoFile = open('info.json', 'r')
dataJSON = json.load(infoFile)
infoFile.close()

api_key = dataJSON["X-API-Key"]
client_id = dataJSON["client_id"]
client_secret = dataJSON["client_secret"]
refresh_token = dataJSON["refresh_token"]
Host = dataJSON["host"]
User = dataJSON["user"]
Password = dataJSON["password"]
Database = dataJSON["database"]

def addAccountsTodb(HEADERS):
    membershipID = getMembership_ID(HEADERS)
    email = input("Enter your Email: ")
    PhoneNumber = input("Enter your Phone Number: ")
    phoneProvider = input("Enter your Phone Provider: ")
    Enum = input("Enter the characters you want to recive notifications for: ")


    con = mysql.connector.connect(
        host=Host,
        user=User,
        password=Password,
        database=Database
    )
    cur = con.cursor()
    query = f"INSERT INTO DestinyVendorUsers.Active_Users (Username, Phone_Number, Provider, MembershipID, CharacterEnum)\
                    VALUES {email, PhoneNumber, phoneProvider, membershipID, Enum};"    
    cur.execute(query)
    con.commit()
    cur.close()
    con.close()


def getMembership_ID(HEADERS):
    gameName = input("Enter your display Name (without the #----) : ")
    code = input("Enter your display code (this is now the #----) : ")
    HEADERS = {"X-API-Key":api_key}
    membershipID = Bungie_Requests.ValidatePlayer(gameName, code, HEADERS)
    return membershipID


def fetchAllIDS():
    con = mysql.connector.connect(
        host=Host,
        user=User,
        password=Password,
        database=Database
    )
    cur = con.cursor()
    cur = con.cursor()
    query = 'SELECT * FROM DestinyVendorUsers.Active_Users'
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    con.close()
    return result
