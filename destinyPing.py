import smtplib
import ssl
from email.message import EmailMessage

import sys

import Bungie_Requests
import database
import Accounts

# the player must check the {Show my progress} box under settings -> Privacy

email_sender = 'destinyvendorsales@gmail.com'
email_password = 'svcfjxzqhnztloec'
emailProviders = {
    "att": "mms.att.net",
    "boost": "myboostmobile.com",
    "cricket": "mms.cricketwireless.net",
    "metro": "mymetropcs.com",
    "sprint": "pm.sprint.com",
    "tmobile": "tmomail.net",
    "verizon": "vzwpix.com",
    "visible": "vzwpix.com"                 
}


def newUser(HEADERS):
     Accounts.addAccountsTodb(HEADERS)

def refreshSales(HEADERS):
    print("---Fetching Vendor Sales---")
    JSONLIST, vendorORDER = Bungie_Requests.fetchAllSales(HEADERS)
    print("---fecthing DONE---")
    print("---updating db---")
    dbList = database.CollectafyData(JSONLIST, vendorORDER)
    database.AddSalesToDB(dbList)
    print("---updating DONE---")

def CheckUsers_SendMessages(HEADERS):
    currentSales = database.readAllSales()
    AccoutList = Accounts.fetchAllIDS()
    for Account in AccoutList:
        collectiblesJSON = Bungie_Requests.fetchPlayerCollection(Account[3], HEADERS)
        print("Checking Collections\n")
        UserMissing = database.checkMissingCollectables(currentSales ,collectiblesJSON, Account[4])
        print(f"\n\n{Account[0]} you are Missing the Following Items: \n")
        body = ""
        for element in UserMissing:
            body = body + f"{element[0]} ({element[2]})\n"
        print(body)

        # quits if there is nothing to send
        if body != "":
            text(body, Account[1], Account[2])

def checkUser(HEADERS, ID):
    currentSales = database.readAllSales()
    collectiblesJSON = Bungie_Requests.fetchPlayerCollection(ID, HEADERS)
    print("Checking Collections\n")
    UserMissing = database.checkMissingCollectables(currentSales ,collectiblesJSON, 256)
    print(f"\n\nID {ID} you are Missing the Following Items: ")
    body = ""
    for element in UserMissing:
        body = body + f"\n{element[0]} ({element[2]})"
    print(body)


        

def text(body, email_receiver, Provider):
    # if there is somthing thats missing end it
    subject = 'You are missing the following:'
    pos = email_receiver.find(")") + 1
    email_receiver = f'{email_receiver[pos:]}@{emailProviders[Provider]}'
    print(email_receiver)
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def main(args):
    mode = args[1]
    if (mode == "-oauthManual"):
        Bungie_Requests.manualOauth()
        print("oauth successfull")
        exit()
    
    HEADERS = Bungie_Requests.updateToken()
    if HEADERS == None: return

    if (HEADERS == None):
        print("Failed to refresh")
        exit()

    if (mode == "-newUser"):
        newUser(HEADERS)
    elif (mode == "-refreshSales"):
        refreshSales(HEADERS)
    elif (mode == "-default"):
        CheckUsers_SendMessages(HEADERS)
    elif (mode == "-User"):
        checkUser(HEADERS, args[2])
    else:
        print("invalid args (only use one)")
        print(f"list of vailid args are {VALID_ARGS}")


VALID_ARGS = ["-refreshSales", "-default", "-oauthManual", "-newUser {username}", "-User {username}"]
if __name__ == '__main__':
    args = sys.argv
    argCount = len(args)
    if(argCount > 1 and argCount < 4):
       main(args) 
    else:
        print("invalid args (only use one)")
        print(f"list of vailid args are {VALID_ARGS}")

sys.stdout.flush()

# command to run every tuesday and friday
#   python3 ~/projects/DestinyVendorSales/simple-api-bungie-destiny.py -refreshSales && python ~/projects/DestinyVendorSales/simple-api-bungie-destiny.py -default
