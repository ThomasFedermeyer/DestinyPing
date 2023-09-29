import requests, zipfile, os, json, sqlite3

# Run this file to downlaod the manifest

def get_manifest():
    manifest_url = 'http://www.bungie.net/Platform/Destiny2/Manifest/'

    #get the manifest location from the json

    infoFile = open('info.json', 'r')
    dataJSON = json.load(infoFile)
    infoFile.close()

    api_key = dataJSON["X-API-Key"]

    HEADERS = {"X-API-Key":api_key}
    r = requests.get(manifest_url,  headers=HEADERS)
    manifest = r.json()
    print(manifest)
    mani_url = 'http://www.bungie.net'+ manifest['Response']['mobileWorldContentPaths']['en']

    #Download the file, write it to 'MANZIP'
    r = requests.get(mani_url)
    with open("MANZIP", "wb") as zip:
        zip.write(r.content)
    print("Download Complete!")

    #Extract the file contents, and rename the extracted file
    # to 'Manifest.content'
    with zipfile.ZipFile('MANZIP') as zip:
        name = zip.namelist()
        zip.extractall()
    os.rename(name[0], 'Manifest.db')
    print('Unzipped!')

hashes = {
    'DestinyAchievementDefinition': 'achievementHash',
    'DestinyActivityDefinition': 'activityHash',
    'DestinyActivityGraphDefinition': 'ActivityGraphHash',
    'DestinyActivityModeDefinition': 'activityModeHash',
    'DestinyActivityModifierDefinition': 'activityModifierHash',
    'DestinyActivityTypeDefinition': 'activityTypeHash',
    'DestinyArtifactDefinition': 'artifactHash',
    'DestinyBondDefinition': 'bondHash',
    'DestinyBreakerTypeDefinition': 'breakerTypeHash',
    'DestinyChecklistDefinition': 'checkListHash',
    'DestinyClassDefinition': 'classHash',
    'DestinyCollectibleDefinition': 'collectibleHash',
    'DestinyDamageTypeDefinition': 'damageTypeHash',
    'DestinyDestinationDefinition': 'destinationHash',
    'DestinyEnergyTypeDefinition': 'energyTypeHash',
    'DestinyEquipmentSlotDefinition': 'EquipmentSlotHash',
    'DestinyEventCardDefinition': 'eventCardHash',
    'DestinyGenderDefinition': 'genderHash',
    'DestinyInventoryBucketDefinition': 'bucketHash',
    'DestinyInventoryItemDefinition': 'itemHash',
    'DestinyProgressionDefinition': 'progressionHash',
    'DestinyRaceDefinition': 'raceHash',
    'DestinyTalentGridDefinition': 'gridHash',
    'DestinyUnlockFlagDefinition': 'flagHash',
    'DestinyHistoricalStatsDefinition': 'statId',
    'DestinyDirectorBookDefinition': 'bookHash',
    'DestinyStatDefinition': 'statHash',
    'DestinySandboxPerkDefinition': 'perkHash',
    'DestinyDestinationDefinition': 'destinationHash',
    'DestinyPlaceDefinition': 'placeHash',
    'DestinyActivityBundleDefinition': 'bundleHash',
    'DestinyStatGroupDefinition': 'statGroupHash',
    'DestinySpecialEventDefinition': 'eventHash',
    'DestinyFactionDefinition': 'factionHash',
    'DestinyVendorCategoryDefinition': 'categoryHash',
    'DestinyEnemyRaceDefinition': 'raceHash',
    'DestinyScriptedSkullDefinition': 'skullHash',
    'DestinyGrimoireCardDefinition': 'cardId'
}

hashes_trunc = {
    'DestinyInventoryItemDefinition': 'itemHash',
    'DestinyTalentGridDefinition': 'gridHash',
    'DestinyHistoricalStatsDefinition': 'statId',
    'DestinyStatDefinition': 'statHash',
    'DestinySandboxPerkDefinition': 'perkHash',
    'DestinyStatGroupDefinition': 'statGroupHash'
}


hash = 1274330687


import sqlite3

# Connect to the database
conn = sqlite3.connect('Manifest.db')

# Create a cursor
cur = conn.cursor()

# Execute the query
cur.execute('SELECT json FROM DestinyInventoryItemDefinition WHERE id = -2097693268')

# Get the hash
jsoninfo = cur.fetchone()[0]
print(jsoninfo)

# Close the connection
conn.close()