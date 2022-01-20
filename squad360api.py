from http import client
import requests
import base64
import os

#Getting Bearer Access token 
#Set a variable for app_short_name with Value 'AppSec'
#Get all the squads and filtering with app_short_name to get the Squad id 
#With Squad id - retrieving all the squad member details
# Here collected only the member aaId as list. 

# username = "115b27f7-ebad-4690-b27f-3fee76aaa412"
# password = "MDVhNWRlYzctNmYyNy00Y2NiLWE3MjQtMmJmODg4Yzg3ZjM1"

#os.environ['client_id'] = "115b27f7-ebad-4690-b27f-3fee76aaa412"
username = os.getenv('user')
password = os.getenv('password')

client_Key_secret = username+":"+password
client_key_secret_enc = base64.b64encode(client_Key_secret.encode()).decode()

headerAuth = {
	'Authorization' : 'Basic '+str(client_key_secret_enc)
}
data = {
	'grant_type' : 'client_credentials'
} 

response = requests.post('https://us-south.appid.cloud.ibm.com/oauth/v4/b6ec3b06-5c05-499d-a409-8761dff5a34d/token', headers = headerAuth, data = data ,verify = True)
bearer_access_token  = response.json()['access_token']

headerDetails = {
    'accept' : 'application/json',
    'Authorization' : 'Bearer '+bearer_access_token
}

class squad360API:

    #Retrieve Squad ID from Squad API - with squad name 
    #With response filtering squad ID for provided squad name
    #https://squad360.mybluemix.net/api/simple/squads  
    def getSquadIdByAppShortName(self,squadName):
        #retrieving all squads and filtering with alias1 (shortname) filter
        allSquads_response  = requests.get('https://squad360.mybluemix.net/api/simple/squads', headers = headerDetails , verify = True )
        for squad in allSquads_response.json():
            if(squad['alias1'] != None and squadName in squad['alias1']):
                squad_id = squad['id']
                return squad_id
            elif(squad['alias2'] != None and squadName in squad['alias2']):
                squad_id = squad['id']
                return squad_id
            elif(squad['name'] != None and squadName in squad['name']):
                squad_id = squad['id']
                return squad_id
        return None

    #Retrieve Squad Member details with Squad Id as input parameter
    ## https://squad360.mybluemix.net/api/simple/squads/{squad_id}/members
    def getSquadMembersBySquadId(self,squad_id):
        print ("Squad Id -> "+str(squad_id))
        squad_member_response = requests.get('https://squad360.mybluemix.net/api/simple/squads/' +str(squad_id)+'/members', headers = headerDetails , verify = True)
        squad_members = squad_member_response.json()['members']
        #list to collect members aaId
        squad_member_ids = []
        #iterating squad members from response
        for member in squad_members:
            squad_member_ids.append(member['aaId'])
        
        return squad_member_ids

    #Retrieve Application details with Short name as input parameter
    #https://squad360.mybluemix.net/api/simple/applications?shortName=AppSec
    def getApplicationsByShortName(self,app_short_name):
        app_details_by_shortName =   requests.get('https://squad360.mybluemix.net/api/simple/applications?shortName=' +app_short_name, headers = headerDetails , verify = True )
        pci_Detail = app_details_by_shortName.json()[0]['pci']
        archer_id = app_details_by_shortName.json()[0]['srcRecId']
        return  app_details_by_shortName.json()

    
    #Check if the Application's PCI value is True or Not with App Short Name as Input parameter
    #  (If True returning 'PCI' otherwise returning 'NON-PCI')
    #https://squad360.mybluemix.net/api/simple/applications?shortName=AppSec
    def checkAppPciVal(self,app_short_name):
        app_details_by_shortName =   requests.get('https://squad360.mybluemix.net/api/simple/applications?shortName=' +app_short_name, headers = headerDetails , verify = True )
        app_details =   app_details_by_shortName.json()
        #here checking PCI value of Application response
        if app_details[0]['pci'] == True:
               return 'PCI'# returning 'PCI' as value equals True
        else:
            return 'NON-PCI'# returning 'NON-PCI' as value other than True 

api = squad360API()

#calling getSquadIdByAppShortName() method to get squad Id  - SQUAD API (v1/api/simple/squads)
#lIST OF aPPLICATION sHORT NAMES BELOW
#1.     1View
#2.     GateReader
#3.     NAVIA
#4.     ADVOCATE
#5.     AppSec

#Relationship b/w Application & SQUAD : Application Short name is equal to squads alias1/alias2/name

#passing App Short name to all the method calls 
app_short_name = 'NAVIA' #<----Change Application Short name here

squadId = api.getSquadIdByAppShortName(app_short_name)
print ("Result for App Short Name : "+app_short_name+"\n")
print ("Squad Detail ")
print("-------------------------------------------------")
#with the squad Id getting all the squad Members AAID as list - SQUAD API (v1/api/simple/squads/{squad_id}/members) 
if(squadId == None):
    print ("No Squad Found")
else:
    squad_member_ids = api.getSquadMembersBySquadId(squadId)
    print ("squad Members AAID -> : "+str(squad_member_ids))

print("\nApplication Details")
print("-------------------------------------------------")
application_details = api.getApplicationsByShortName(app_short_name)
print ("ShortName -> :"+str(application_details[0]['shortName']) + "  pci -> :"+str(application_details[0]['pci']) + "  archer_id -> : "+ str(application_details[0]['srcRecId']) )
print("-----------------------------------") 

#App with PCI value as True
app_pci_desc = api.checkAppPciVal(app_short_name)
#printing the Application PCI value returned from checkAppPciVal() method call
print (str(app_pci_desc))
